from groq import Groq
from config import GROQ_API_KEY
from firebase import get_student, create_student, update_student, increment_session

client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = """You are Wax, a personal tutor for Nigerian secondary school students built by WaxPrep.

YOUR NAME: Wax. Never call yourself anything else. Never say you are an AI or bot.

LANGUAGE: Speak clear simple English. Only add small Pidgin words occasionally when the student uses Pidgin. Never speak full Pidgin sentences.

PERSONALITY: Warm, patient, encouraging. Never make a student feel stupid. Celebrate small wins.

TEACHING RULES:
- Never assume the student knows anything. Start from zero always.
- Use Nigerian examples like meat pie, NEPA, danfo bus.
- Keep responses short, max 3 short paragraphs.
- Ask ONE question at a time.
- When student is wrong say: Almost! Let me show you another way.

NEVER:
- Call yourself any other name
- Say you are an AI or bot
- Discuss sex or inappropriate topics, redirect firmly but kindly
- Write walls of text

SUBJECTS: Physics, Chemistry, Biology, Mathematics, English, Economics, Government, Literature, Geography for JAMB, WAEC, NECO, BECE.

CRISIS: If student mentions self-harm say: I hear you and I am glad you told me. Please call Mentally Aware Nigeria Initiative 08091116264"""


def get_wax_reply(message, system_extra=""):
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT + system_extra},
            {"role": "user", "content": message}
        ],
        max_tokens=1000
    )
    return completion.choices[0].message.content


def get_wax_response(phone_number, message, message_type="text"):

    if message_type == "audio":
        return "Hey! I can only read text for now. Type your question and I will help you 😊"
    if message_type == "image":
        return "Hey! I cannot view images yet. Type your question and I will help you 😊"

    student = get_student(phone_number)

    if not student:
        student = create_student(phone_number)
        return get_wax_reply(
            "A brand new student just messaged WaxPrep for the very first time. Introduce yourself as Wax warmly in 2 short sentences. Then ask: What is your first name?"
        )

    step = student.get("onboarding_step", "awaiting_name")

    if step == "awaiting_name":
        name = message.strip().title()
        wax_id = student.get("wax_id")
        update_student(phone_number, {
            "name": name,
            "onboarding_step": "awaiting_class"
        })
        return get_wax_reply(
            f"The student's name is {name}. Their WaxID is {wax_id}. Welcome them by name warmly in 1 sentence. Tell them their WaxID is {wax_id} and to save it. Then ask: What class are you in? Give these examples: JSS1, JSS2, JSS3, SS1, SS2, SS3, or Out of school."
        )

    if step == "awaiting_class":
        update_student(phone_number, {
            "class_level": message.strip(),
            "onboarding_step": "awaiting_goal"
        })
        name = student.get("name", "")
        return get_wax_reply(
            f"Student {name} is in {message}. Now ask them ONE question: What do you want to use WaxPrep for? Give these 4 options numbered: 1. Prepare for JAMB, WAEC or NECO. 2. Improve my school grades. 3. Understand a difficult topic. 4. General learning."
        )

    if step == "awaiting_goal":
        update_student(phone_number, {
            "learning_goal": message.strip(),
            "onboarding_step": "awaiting_subjects"
        })
        name = student.get("name", "")
        return get_wax_reply(
            f"Student {name} said their goal is: {message}. Now ask them: Which subjects do you need help with? They can name more than one."
        )

    if step == "awaiting_subjects":
        subjects = [s.strip() for s in message.replace(",", " ").split()]
        update_student(phone_number, {
            "subjects": subjects,
            "onboarding_step": "awaiting_study_time"
        })
        name = student.get("name", "")
        return get_wax_reply(
            f"Student {name} needs help with: {message}. Now ask them ONE question: When do you usually study? Morning, afternoon, or night?"
        )

    if step == "awaiting_study_time":
        update_student(phone_number, {
            "study_time": message.strip(),
            "onboarding_step": "complete",
            "onboarding_complete": True
        })
        increment_session(phone_number)
        name = student.get("name", "")
        subjects = student.get("subjects", [])
        goal = student.get("learning_goal", "")
        return get_wax_reply(
            f"Onboarding complete for {name}. Goal: {goal}. Subjects: {subjects}. Study time: {message}. Welcome them fully in 2 short sentences, summarize what you know about them, then ask: What topic do you want to start with today?"
        )

    increment_session(phone_number)
    name = student.get("name", "")
    class_level = student.get("class_level", "")
    goal = student.get("learning_goal", "")
    subjects = ", ".join(student.get("subjects", []))

    profile = f"\n\nSTUDENT PROFILE: Name: {name}. Class: {class_level}. Goal: {goal}. Subjects: {subjects}. Always address them by name. You already know them, never ask for their details again."

    return get_wax_reply(message, profile)
