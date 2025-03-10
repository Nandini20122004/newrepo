import google.generativeai as genai

genai.configure(api_key="AIzaSyD7q_078StneW-FXIDnIYc9DfYO3YwLEQM")
model = genai.GenerativeModel("gemini-2.0-flash")

def get_ai_answer(question):
    response = model.generate_content(question)
    return response.text if response else "AI couldn't answer."