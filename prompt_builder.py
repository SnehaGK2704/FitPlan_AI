def calculate_bmi(weight, height):
    height_m = height / 100
    return weight / (height_m ** 2)


def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal Weight"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"


def build_prompt(name, gender, height, weight, goal, fitness_level, equipment):

    bmi = calculate_bmi(weight, height)
    bmi_status = bmi_category(bmi)

    equipment_list = ", ".join(equipment) if equipment else "No Equipment"

    prompt = f"""
You are a certified professional fitness trainer.

Generate a **5-day personalized workout plan** based on the user profile below.

USER PROFILE
Name: {name}
Gender: {gender}
Height: {height} cm
Weight: {weight} kg
BMI: {bmi:.2f} ({bmi_status})
Goal: {goal}
Fitness Level: {fitness_level}
Available Equipment: {equipment_list}

INSTRUCTIONS

1. Create a workout plan for **5 days (Day 1 to Day 5)**.
2. Each day must target a **specific muscle group**.
3. Each day must contain **4 exercises**.
4. For each exercise include:
   - Exercise name
   - Sets
   - Reps
   - Rest time
5. Adjust difficulty based on **fitness level and BMI category**.
6. Avoid unsafe or extremely advanced exercises for beginners.
7. Exercises must be realistic and can be performed at home or gym based on available equipment.

OUTPUT FORMAT

Day 1 – <Muscle Group>

Exercise: <Exercise Name>
Sets: X
Reps: X
Rest: X seconds

Exercise: <Exercise Name>
Sets: X
Reps: X
Rest: X seconds

Repeat until Day 5.

IMPORTANT:
Return ONLY the workout plan.
Do NOT include explanations or extra text.
"""

    return prompt, bmi, bmi_status