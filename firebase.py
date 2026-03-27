import firebase_admin
from firebase_admin import credentials, firestore
import os
import json
import random
import string
from datetime import datetime

# Initialize Firebase
cred_json = os.getenv("FIREBASE_CREDENTIALS")
cred_dict = json.loads(cred_json)
cred = credentials.Certificate(cred_dict)
firebase_admin.initialize_app(cred)

db = firestore.client()

def generate_wax_id():
    chars = string.ascii_uppercase + string.digits
    unique = ''.join(random.choices(chars, k=5))
    return f"WAX-{unique}"

def get_student(phone_number):
    doc = db.collection("students").document(phone_number).get()
    if doc.exists:
        return doc.to_dict()
    return None

def create_student(phone_number):
    wax_id = generate_wax_id()
    student = {
        "phone_number": phone_number,
        "wax_id": wax_id,
        "name": None,
        "class_level": None,
        "school_type": None,
        "learning_goal": None,
        "target_exam": None,
        "exam_date": None,
        "subjects": [],
        "weak_topics": {},
        "preferred_language": "english",
        "study_time": None,
        "session_count": 0,
        "last_active": datetime.now().isoformat(),
        "onboarding_complete": False,
        "onboarding_step": "awaiting_name",
        "subscription": "free_trial",
        "trial_start": datetime.now().isoformat(),
        "created_at": datetime.now().isoformat()
    }
    db.collection("students").document(phone_number).set(student)
    return student

def update_student(phone_number, updates):
    updates["last_active"] = datetime.now().isoformat()
    db.collection("students").document(phone_number).update(updates)

def increment_session(phone_number):
    student = get_student(phone_number)
    if student:
        update_student(phone_number, {
            "session_count": student.get("session_count", 0) + 1
        })
