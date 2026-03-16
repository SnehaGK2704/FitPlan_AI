from flask import Flask, render_template, request, redirect, session
import sqlite3

from database import create_tables
from auth import verify_user, register_user, update_profile
from email_utils import init_mail, generate_otp, send_otp

from prompt_builder import build_prompt
from model_api import query_model

app = Flask(__name__)
app.secret_key = "fitplan_secret_key"

# Initialize mail
init_mail(app)

# Create database tables
create_tables()


#------------------Parsing Workout Plan------------------
def parse_workout_plan(plan_text):

    days = []
    current_day = None

    lines = plan_text.split("\n")

    for line in lines:
        line = line.strip()

        if line.startswith("Day"):
            if current_day:
                days.append(current_day)

            current_day = {
                "title": line,
                "exercises": []
            }

        elif line.startswith("Exercise:"):
            exercise_name = line.replace("Exercise:", "").strip()

            current_day["exercises"].append({
                "name": exercise_name,
                "sets": "",
                "reps": "",
                "rest": ""
            })

        elif line.startswith("Sets:"):
            current_day["exercises"][-1]["sets"] = line.replace("Sets:", "").strip()

        elif line.startswith("Reps:"):
            current_day["exercises"][-1]["reps"] = line.replace("Reps:", "").strip()

        elif line.startswith("Rest:"):
            current_day["exercises"][-1]["rest"] = line.replace("Rest:", "").strip()

    if current_day:
        days.append(current_day)

    return days


# ---------------- LOGIN ----------------

@app.route("/", methods=["GET", "POST"])
def login():

    error = None

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = verify_user(email, password)

        if user:

            otp = generate_otp()

            session["otp"] = otp
            session["temp_user"] = user

            send_otp(app, email, otp)

            return redirect("/verify-otp")

        else:
            error = "Invalid email or password"

    return render_template("login.html", error=error)


# ---------------- OTP VERIFICATION ----------------

@app.route("/verify-otp", methods=["GET", "POST"])
def verify_otp():

    error = None

    if request.method == "POST":

        user_otp = request.form["otp"]

        if user_otp == session.get("otp"):

            user = session.get("temp_user")

            session["user_id"] = user[0]
            session["name"] = user[3]

            if user[3] is None or user[4] is None or user[5] is None or user[6] is None:
                return redirect("/setup-profile")

            return redirect("/home")

        else:
            error = "Invalid OTP"

    return render_template("verify_otp.html", error=error)


# ---------------- SIGNUP ----------------

@app.route("/signup", methods=["GET", "POST"])
def signup():

    error = None

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        try:
            register_user(email, password)
            return redirect("/")

        except sqlite3.IntegrityError:
            error = "Email already registered. Please login."

    return render_template("signup.html", error=error)


# ---------------- PROFILE SETUP ----------------

@app.route("/setup-profile", methods=["GET", "POST"])
def setup_profile():

    if "user_id" not in session:
        return redirect("/")

    if request.method == "POST":

        name = request.form["name"]
        age = request.form["age"]
        height = request.form["height"]
        weight = request.form["weight"]

        update_profile(session["user_id"], name, age, height, weight)

        session["name"] = name
        session["age"] = age
        session["height"] = height
        session["weight"] = weight

        return redirect("/home")

    return render_template("setup_profile.html")


# ---------------- HOME DASHBOARD ----------------

@app.route("/home")
def home():

    if "user_id" not in session:
        return redirect("/")

    user_id = session["user_id"]

    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # get user stats
    cur.execute("""
        SELECT name, weight, height
        FROM users
        WHERE id=?
    """, (user_id,))

    user = cur.fetchone()

    name = user["name"]
    weight = user["weight"]
    height = user["height"]

    # BMI calculation
    bmi = round(weight / ((height/100) ** 2), 1)

    # count plans generated
    cur.execute("""
        SELECT COUNT(*) as total
        FROM workout_plans
        WHERE user_id=?
    """, (user_id,))

    plans_completed = cur.fetchone()["total"]

    # get latest workout plan
    cur.execute("""
        SELECT plan
        FROM workout_plans
        WHERE user_id=?
        ORDER BY created_at DESC
        LIMIT 1
    """, (user_id,))

    plan_row = cur.fetchone()

    exercises = []

    if plan_row:

        plan_text = plan_row["plan"]

        current_exercise = None

        for line in plan_text.split("\n"):

            line = line.strip()

            if line.startswith("Exercise"):
                current_exercise = line.replace("Exercise:", "").strip()

            elif line.startswith("Reps") and current_exercise:
                reps = line.replace("Reps:", "").strip()
                exercises.append(f"{current_exercise} – {reps} reps")
                current_exercise = None

    # show only first 4 exercises for today's goals
    exercises = exercises[:4]

    # fetch weight history
    cur.execute("""
        SELECT weight, log_date
        FROM weight_logs
        WHERE user_id=?
        ORDER BY log_date
    """, (user_id,))

    rows = cur.fetchall()

    weight_data = [row["weight"] for row in rows]
    weight_dates = [row["log_date"] for row in rows]

    conn.close()

    return render_template(
        "index.html",
        name=name,
        weight=weight,
        bmi=bmi,
        plans_completed=plans_completed,
        exercises=exercises,
        weight_data=weight_data,
        weight_dates=weight_dates
    )





# ---------------- GENERATE WORKOUT ----------------

@app.route("/generate", methods=["GET", "POST"])
def generate():

    if "user_id" not in session:
        return redirect("/")

    user_id = session["user_id"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name, age, height, weight
        FROM users
        WHERE id=?
    """, (user_id,))

    user = cursor.fetchone()

    conn.close()

    if not user:
        return "User profile not found."

    name, age, height, weight = user


    if request.method == "GET":
        return render_template("generate.html")


    goal = request.form["goal"]
    fitness_level = request.form["fitness_level"]
    equipment = request.form.getlist("equipment")

    equipment_str = ", ".join(equipment)

    gender = "Not Specified"

    prompt, bmi, bmi_status = build_prompt(
        name=name,
        gender=gender,
        height=float(height),
        weight=float(weight),
        goal=goal,
        fitness_level=fitness_level,
        equipment=equipment
    )

    prompt += f"\nAge: {age}"

    plan = query_model(prompt)

    workout_days = parse_workout_plan(plan)

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO workout_plans
    (user_id, goal, fitness_level, equipment, plan)
    VALUES (?, ?, ?, ?, ?)
    """,
    (user_id, goal, fitness_level, equipment_str, plan)
    )

    conn.commit()
    conn.close()

    return render_template(
        "result.html",
        workout_days=workout_days,
        bmi=bmi,
        bmi_status=bmi_status
    )


# ---------------- VIEW CURRENT WORKOUT ----------------

@app.route("/current-workout")
def current_workout():

    if "user_id" not in session:
        return redirect("/")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT plan FROM workout_plans
        WHERE user_id=?
        ORDER BY id DESC
        LIMIT 1
    """, (session["user_id"],))

    plan = cursor.fetchone()

    conn.close()

    if not plan:
        return render_template("current_workout.html", workout_days=None)

    parsed_plan = parse_workout_plan(plan[0])

    return render_template(
        "current_workout.html",
        workout_days=parsed_plan
    )


# ---------------- PREVIOUS PLANS ----------------

@app.route("/previous-plans")
def previous_plans():

    if "user_id" not in session:
        return redirect("/")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT plan FROM workout_plans
        WHERE user_id=?
        ORDER BY id DESC
    """, (session["user_id"],))

    plans = cursor.fetchall()
    conn.close()

    parsed_plans = []

    for p in plans:
        parsed = parse_workout_plan(p[0])
        parsed_plans.append(parsed)

    return render_template(
        "previous_plans.html",
        parsed_plans=parsed_plans
    )

#----------------- WEIGHT LOGS-----------------
@app.route("/log_weight", methods=["POST"])
def log_weight():

    if "user_id" not in session:
        return redirect("/")

    weight = request.form["weight"]
    user_id = session["user_id"]

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO weight_logs (user_id, weight)
    VALUES (?,?)
    """,(user_id, weight))

    conn.commit()
    conn.close()

    return redirect("/home")


# ---------------- LOGOUT ----------------

@app.route("/logout")
def logout():

    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)