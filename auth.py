from database import get_db


def verify_user(email, password):

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (email, password)
    )

    user = cursor.fetchone()
    conn.close()

    return user


def register_user(email, password):

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users(email,password) VALUES(?,?)",
        (email, password)
    )

    conn.commit()
    conn.close()


def update_profile(user_id, name, age, height, weight):

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE users
    SET name=?, age=?, height=?, weight=?
    WHERE id=?
    """, (name, age, height, weight, user_id))

    conn.commit()
    conn.close()