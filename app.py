import streamlit as st
import firebase_admin
from firebase_admin import auth, credentials, firestore
import json
import smtplib
from twilio.rest import Client
from datetime import datetime
import threading
from study_planner import generate_study_plan, get_study_progress
from ai_chat import get_ai_answer
from dotenv import load_dotenv
import os

import streamlit as st

st.set_page_config(page_title="StudBud: AI Study Planner", page_icon="📚")  # Ensure the logo file is in the same directory
st.title("📚 StudBud: AI Study Planner")


# Initialize Firebase **ONLY IF NOT ALREADY INITIALIZED**
if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()
load_dotenv("key.env")  # If your file is named .env, just use load_dotenv()

EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")


# Function to send email notifications
def send_email(to_email, subject, message):
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        msg = f"Subject: {subject}\n\n{message}"
        server.sendmail(EMAIL_SENDER, to_email, msg)
        server.quit()
        return True
    except Exception as e:
        return f"Email error: {e}"

# Function to send SMS notifications
def send_sms(to_phone, message):
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        client.messages.create(body=message, from_=TWILIO_PHONE_NUMBER, to=to_phone)
        return True
    except Exception as e:
        return f"SMS error: {e}"

# Function to send notifications at the scheduled time
def send_notifications(user_id, plan):
    user_doc = db.collection("users").document(user_id).get()
    if user_doc.exists:
        user_data = user_doc.to_dict()
        email = user_data.get("email")
        phone = user_data.get("phone")

        message = f"📢 Study Reminder!\nSubject: {plan['subject']}\nDuration: {plan['duration']} mins"

        send_email(email, "Study Reminder", message)
        send_sms(phone, message)

# Function to schedule notifications
def schedule_notifications(user_id, study_plan):
    for plan in study_plan:
        study_time = datetime.strptime(plan["time"], "%H:%M").replace(
            year=datetime.now().year, month=datetime.now().month, day=datetime.now().day
        )
        now = datetime.now()

        if study_time > now:
            delay = (study_time - now).total_seconds()
            threading.Timer(delay, send_notifications, args=(user_id, plan)).start()

# Initialize session state
if "study_plan" not in st.session_state:
    st.session_state.study_plan = []

# App Title
st.write("Plan, track, and optimize your study sessions with AI.")

# Sidebar User Input
# Removed the name input option
# username = st.sidebar.text_input("Enter your name:")
# if username:
#     st.sidebar.write(f"Welcome, {username}!")

# User Authentication
if "user" not in st.session_state:
    page = st.selectbox("Choose an option", ["Login", "Signup"])
    if page == "Login":
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            try:
                user = auth.get_user_by_email(email)
                st.session_state["user"] = {"uid": user.uid, "email": email}
                st.success("Login successful!")
                st.rerun()
            except firebase_admin.auth.UserNotFoundError:
                st.error("Invalid email or password.")
    else:
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        name = st.text_input("Full Name")
        age = st.number_input("Age", min_value=10, max_value=100)
        phone = st.text_input("Mobile Number")
        if st.button("Signup"):
            try:
                user = auth.create_user(email=email, password=password)
                db.collection("users").document(user.uid).set({
                    "name": name,
                    "email": email,
                    "age": age,
                    "phone": phone
                })
                st.success("Signup successful! Please log in.")
            except Exception as e:
                st.error(f"Error: {e}")
else:
    st.sidebar.write(f"Welcome, {st.session_state['user']['email']}! 🎓")
    if st.sidebar.button("Logout"):
        st.session_state.pop("user")
        st.rerun()

    # Study Plan Generation
    st.subheader("📝 Generate Study Plan")
    subject = st.text_input("Enter Subject:")
    study_hours = st.slider("Study Hours per Day:", 1, 12, 2)
    days = st.number_input("Number of Days:", min_value=1, max_value=30, value=7)

    if st.button("Generate Plan"):
        if subject and study_hours and days:
            study_plan = generate_study_plan(subject, study_hours, days)
            st.session_state.study_plan.append(study_plan)
            st.success("Study plan generated!")
            st.write(study_plan["plan"])
        else:
            st.error("Please fill in all fields.")

    # Study Progress Tracker
    st.subheader("📊 Track Your Progress")
    progress = get_study_progress(st.session_state.study_plan)
    st.write(progress)

    # AI Chat for Study Assistance
    st.subheader("🤖 Ask AI Your Study Questions")
    question = st.text_area("Type your question:")
    if st.button("Get Answer"):
        if question:
            answer = get_ai_answer(question)
            st.write(answer)
        else:
            st.error("Please enter a question.")
