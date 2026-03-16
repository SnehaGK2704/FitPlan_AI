# 🏋️ FitPlan AI – Personalized Fitness Plan Generator

## 📌 Project Overview
FitPlan AI is an intelligent web application that generates personalized workout plans based on a user's physical attributes and fitness goals.

The system uses Artificial Intelligence and Machine Learning to analyze user inputs such as age, height, weight, and fitness level to generate customized workout routines. The goal of this project is to make fitness guidance accessible to everyone without needing a personal trainer.

The platform provides structured fitness plans along with daily goals and progress tracking to help users stay consistent and motivated.

---

# 🎯 Problem Statement
Many people want to improve their fitness but face several challenges:

- Lack of personalized workout guidance
- Expensive personal trainers
- Generic workout routines that do not match individual fitness levels
- Lack of motivation and structured progress tracking

FitPlan AI solves these problems by generating personalized workout plans using AI.

---

# 💡 Solution
FitPlan AI generates dynamic fitness plans based on user data.

The system collects user information during profile setup and processes it using an AI model to generate a structured workout plan.

The solution provides:

- Personalized workout recommendations
- Daily fitness goals
- Progress tracking dashboard
- User authentication with OTP verification
- Database storage for user profiles

---

# 🧠 Key Features

## 🔐 Authentication System
- Secure Signup and Login
- OTP Verification for account authentication
- User data stored in a database

## 👤 Profile Setup
Users provide information such as:

- Name
- Age
- Height
- Weight
- Fitness Level

This data is used by the AI system to generate personalized workout plans.

## 🤖 AI-Based Workout Plan Generation
The AI model analyzes user inputs and generates a structured workout plan tailored to the user's fitness level.

## 📊 Interactive Dashboard
The dashboard displays:

- Generated fitness plan
- Daily workout goals
- Progress trackers
- Visual progress representation using charts

## 📅 Daily Goal System
The system generates daily workout goals that complement the overall fitness plan.

## 📈 Progress Tracking
Two progress trackers help users stay motivated:

- Workout Plan Progress
- Daily Goal Completion

---

# 🏗️ System Architecture

User Interface (HTML, CSS, JavaScript)
        │
        ▼
Flask Backend (Python)
        │
        ▼
Authentication System (Login + OTP)
        │
        ▼
Database (User Profile Storage)
        │
        ▼
AI Model / API
        │
        ▼
Workout Plan Generator
        │
        ▼
Dashboard with Progress Tracking

---

# ⚙️ Technology Stack

## Frontend
- HTML
- CSS
- JavaScript
- Chart.js (for progress visualization)

## Backend
- Python
- Flask

## Database
- SQLite / MySQL

## AI / Model
- Machine Learning based fitness plan generator
- API integration for AI model

---

# 🔄 Project Workflow

## 1️⃣ User Registration
Users create an account using their email and password.

## 2️⃣ OTP Verification
An OTP verification step ensures secure authentication.

## 3️⃣ User Login
Once verified, users can log in to their account.

## 4️⃣ Profile Setup
Users enter their personal and fitness-related details.

## 5️⃣ AI Plan Generation
The system sends the user data to the AI model which generates a personalized fitness plan.

## 6️⃣ Dashboard Display
The generated plan is displayed on the dashboard along with daily goals and progress trackers.

---

# 🌍 Impact
FitPlan AI aims to make fitness guidance accessible and personalized for everyone.

Benefits include:

- Encourages healthier lifestyles
- Provides structured workout guidance
- Reduces dependency on expensive trainers
- Promotes consistency through goal tracking

---

# 🚀 Future Improvements

- Nutrition plan integration
- AI-based progress adaptation
- Mobile application
- Wearable device integration
- Real-time workout feedback

---

# 🖥️ Installation & Setup

## 1️⃣ Clone the repository

```bash
git clone [https://github.com/your-username/fitplan-ai.git](https://github.com/SnehaGK2704/FitPlan_AI.git)
cd fitplan-ai
```

## 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

## 3️⃣ Run the Flask application

```bash
python app.py
```

## 4️⃣ Open in browser

http://127.0.0.1:5000

---

# 📸 Screenshots



Example:

![Dashboard](screenshots/dashboard.png)

![Workout Plan](screenshots/plan.png)

---

# 👨‍💻 Contributors

- Sneha GK

---

# 📜 License

This project is developed for educational and research purposes.
