AI Study Planner

Overview

The AI Study Planner is a smart application designed to help students optimize their study sessions using AI-driven study plans, progress tracking, and AI-powered assistance. It integrates Firebase authentication, Firestore for data storage, and Twilio for SMS notifications. Additionally, it allows email notifications for study reminders.

Features

User Authentication: Signup/Login using Firebase authentication.

Study Plan Generator: AI-based study plan generation based on subjects and available study hours.

Study Progress Tracker: Monitors and tracks study progress over time.

AI Chat Assistant: Provides AI-powered responses to study-related queries.

Email & SMS Notifications: Sends reminders for scheduled study sessions.

Technologies Used

Python

Streamlit (for the UI)

Firebase Admin SDK (for authentication and database management)

Firestore (for storing user data and study plans)

Twilio (for sending SMS notifications)

SMTP (Gmail) (for sending email notifications)

dotenv (for environment variable management)

Threading (for scheduling notifications)

Installation & Setup

Prerequisites

Ensure you have Python installed along with the required dependencies.

Clone the Repository

 git clone <repository-url>
 cd ai-study-planner

Install Dependencies

pip install streamlit firebase-admin twilio python-dotenv

Firebase Setup

Create a Firebase project at Firebase Console.

Enable Authentication and Firestore Database.

Download the serviceAccountKey.json and place it in the project directory.

Environment Variables

Create a .env file in the root directory and add:

EMAIL_SENDER=your-email@gmail.com
EMAIL_PASSWORD=your-email-password
TWILIO_ACCOUNT_SID=your-twilio-account-sid
TWILIO_AUTH_TOKEN=your-twilio-auth-token
TWILIO_PHONE_NUMBER=your-twilio-phone-number

Running the Application

To start the application, run:

streamlit run app.py

Usage

Login or Sign up to create an account.

Generate a Study Plan by entering a subject, daily study hours, and the number of study days.

Track Study Progress to monitor your improvements.

Ask AI Questions related to your studies for instant help.

Receive Notifications via email or SMS as reminders.

Contribution

Feel free to fork the repository and make contributions via pull requests.

License

This project is open-source and available under the MIT License.

run the following command in your terminal to start the application: streamlit run app.py
After login only you can see the study plan and track study progress. If you want to see the study plan and track study progress of other users then you have to be admin. To become admin you have to contact the admin of