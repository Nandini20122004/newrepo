import google.generativeai as genai

genai.configure(api_key="AIzaSyD7q_078StneW-FXIDnIYc9DfYO3YwLEQM")
model = genai.GenerativeModel("gemini-2.0-flash")

def generate_study_plan(subject, study_hours, days):
    query = f"Create a {days}-day study plan for {subject} with {study_hours} hours per day."
    response = model.generate_content(query)
    return {"subject": subject, "study_hours": study_hours, "days": days, "plan": response.text if response else "AI couldn't generate a plan."}

def get_study_progress(study_plans):
    if not study_plans:
        return "No study plans yet. Generate one above."
    progress_text = ""
    for idx, plan in enumerate(study_plans):
        progress_text += f"{plan['subject']} - {plan['days']} days\n"
    return progress_text