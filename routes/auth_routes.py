from flask import Blueprint, render_template, request, redirect, url_for, session
from models.db import get_db   # unified DB access
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint("auth", __name__)

# ---------------- LOGIN ----------------
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT role, password FROM users WHERE username=?", (username,))
        user = cur.fetchone()

        if user and check_password_hash(user[1], password):
            session["user"] = username
            session["role"] = user[0]

            # Fetch student name if exists
            cur.execute(
                "SELECT student_name FROM students WHERE enrollment_no=?",
                (username,)
            )
            student = cur.fetchone()
            if student:
                session["name"] = student[0]

            conn.close()

            if user[0] == "admin":
                return redirect("/admin")
            elif user[0] == "faculty":
                return redirect("/faculty")
            else:
                return redirect("/student")
        else:
            error = "Invalid Credentials"
            conn.close()

    return render_template("login.html", error=error)


# ---------------- LOGOUT ----------------
@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))


# ---------------- PROFILE ----------------
@auth_bp.route("/profile")
def profile():
    if "user" not in session:
        return redirect(url_for("auth.login"))

    username = session.get("user")

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT username, role FROM users WHERE username=?", (username,))
    user = cur.fetchone()
    conn.close()

    return render_template("profile.html", user=user)


# ---------------- CHANGE PASSWORD ----------------
@auth_bp.route("/change-password", methods=["GET", "POST"])
def change_password():
    if "user" not in session:
        return redirect(url_for("auth.login"))

    message = None
    error = None

    if request.method == "POST":
        current = request.form["current_password"]
        new = request.form["new_password"]
        username = session.get("user")

        conn = get_db()
        cur = conn.cursor()

        cur.execute(
            "SELECT password FROM users WHERE username=?",
            (username,)
        )

        db_password = cur.fetchone()[0]

        if not check_password_hash(db_password, current):
            error = "Current password incorrect"
        else:
            hashed_new = generate_password_hash(new)

            cur.execute(
                "UPDATE users SET password=? WHERE username=?",
                (hashed_new, username)
            )

            conn.commit()
            message = "Password updated successfully"

        conn.close()

    return render_template(
        "change_password.html",
        message=message,
        error=error
    )


# ---------------- ACCOUNT SETTINGS ----------------
@auth_bp.route("/account-settings", methods=["GET", "POST"])
def account_settings():

    if "user" not in session:
        return redirect(url_for("auth.login"))

    username = session.get("user")

    conn = get_db()
    cur = conn.cursor()

    message = None

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]

        cur.execute("""
        UPDATE students
        SET student_name=?, email=?, phone=?
        WHERE enrollment_no=?
        """, (name, email, phone, username))

        conn.commit()

        # update session so header changes instantly
        session["name"] = name

        message = "Profile updated successfully"

    cur.execute("""
        SELECT student_name, email, phone, program, batch
        FROM students
        WHERE enrollment_no=?
    """, (username,))

    user = cur.fetchone()

    if user is None:
        user = ["", "", "", "", ""]

    conn.close()

    return render_template(
        "account_settings.html",
        user=user,
        message=message
    )

@auth_bp.route("/dashboard")
def dashboard_redirect():

    if "user" not in session:
        return redirect(url_for("auth.login"))

    role = session.get("role")

    if role == "admin":
        return redirect("/admin")

    elif role == "faculty":
        return redirect("/faculty")

    else:
        return redirect("/student")