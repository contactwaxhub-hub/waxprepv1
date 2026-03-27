from groq import Groq
from config import GROQ_API_KEY
from firebase import get_student, create_student, update_student, increment_session

client = Groq(api_key=GROQ_API_KEY)

ONBOARDING_STEPS = {
    "awaiting_name": "Ask for their first name warmly. Introduce yourself as Wax first.",
    "awaiting_class": "Ask what class they are in. Give examples: JSS1, JSS2, JSS3, SS1, SS2, SS3.",
    "awaiting_goal": "Ask what they want to use WaxPrep for. Give options: Prepare for WAEC/JAMB/NECO, Improve grades, Understand a topic, General learning.",
    "awaiting_subjects": "Ask which subjects they need the most help with.",
    "awaiting_study_time": "Ask when they usually study. Morning, afternoon, or night.",
    "complete": ""
}

def handle_onboarding(student, message):
    step = student.get("onboarding_step", "awaiting_name")
    phone = student["phone_number"]

    if step == "awaiting_name":
        update_student(phone, {
            "name": message.strip().title(),
            "onboarding_step": "awaiting_class"
        })
        return get_wax_reply(
            f"Student just told me their name is {message}. Welcome them warmly by name, tell them their WaxID is {student['wax_id']}, tell them to save it, then ask what class they are in.",
            student
        )

    elif step == "awaiting_class":
        update_student(phone, {
            "class_level": message.strip(),
            "onboarding_step": "awaiting_goal"
        })
        return get_wax_reply(
            f"Student is in {message}. Now ask what they want to use WaxPrep for. Options: Prepare for WAEC/JAMB/NECO, Improve school grades, Understand a difficult topic, General learning.",
            student
        )

    elif step == "awaiting_goal":
        update_student(phone, {
            "learning_goal": message.strip(),
            "onboarding_step": "awaiting_subjects"
        })
        return get_wax_reply(
            f"Student's goal is {message}. Now ask which subjects they need the most help with.",
            student
        )

    elif step == "awaiting_subjects":
        update_student(phone, {
            "subjects": [s.strip() for s in message.split(",")],
            "onboarding_step": "awaiting_study_time"
        })
        return get_wax_reply(
            f"Student needs help with {message}. Now ask when they usually study: morning, afternoon or night.",
            student
        )

    elif step == "awaiting_study_time":
        update_student(phone, {
            "study_time": message.strip(),
            "onboarding_step": "complete",
            "onboarding_complete": True
        })
        increment_session(phone)
        return get_wax_reply(
            f"Onboarding is complete. Student studies in the {message}. Now welcome them fully, summarize what you know about them, and ask what topic they want to start with today.",
            student
        )

    return get_wax_reply(message, student)


def get_wax_reply(message, student=None):
    system = """You are Wax, a personal AI tutor for Nigerian secondary school students built by WaxPrep.
YOUR NAME: Wax. Never call yourself anything else. Never say you are an AI or bot.
PERSONALITY: Warm, patient, encouraging. Mix English and Pidgin based on how the student talks.
Never make a student feel stupid. Celebrate small wins.
TEACHING RULES: Never assume the student knows anything. Start from zero always.
Use Nigerian examples like meat pie, NEPA, danfo bus.
Keep responses short, max 3 short paragraphs. Ask ONE question at a time.
When student is wrong say: Almost! Let me show you another way.
NEVER discuss sex or inappropriate topics, redirect firmly but kindly.
SUBJECTS: Physics, Chemistry, Biology, Mathematics, English, Economics, Government, Literature, Geography for JAMB, WAEC, NECO, BECE.
CRISIS: If student mentions self-harm say: I hear you and I am glad you told me. Please call Mentally Aware Nigeria Initiative 08091116264"""

    if student and student.get("onboarding_complete"):
        name = student.get("name", "")
        class_level = student.get("class_level", "")
        goal = student.get("learning_goal", "")
        subjects = ", ".join(student.get("subjects", []))
        system += f"\n\nSTUDENT PROFILE: Name: {name}. Class: {class_level}. Goal: {goal}. Subjects: {subjects}. Always address them by name. You already know them, never ask for their details again."

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": message}
        ],
        max_tokens=1000
    )
    return completion.choices[0].message.content


def get_wax_response(phone_number, message):
    student = get_student(phone_number)

    if not student:
        student = create_student(phone_number)
        return get_wax_reply(
            "A brand new student just messaged WaxPrep for the first time. Introduce yourself as Wax warmly, tell them WaxPrep is their personal tutor, then ask for their first name.",
            student
        )

    if not student.get("onboarding_complete"):
        return handle_onboarding(student, message)

    increment_session(phone_number)
    return get_wax_reply(message, student)
