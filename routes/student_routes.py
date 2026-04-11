from flask import Blueprint, render_template, session, redirect, url_for
from models.db import get_db

student_bp = Blueprint("student", __name__)

# ---------------- STUDENT DASHBOARD ----------------
@student_bp.route("/student")
def student_dashboard():

    # Check login and role
    if "user" not in session or session.get("role") != "student":
        return redirect(url_for("auth.login"))

    enrollment_no = session.get("user")

    conn = get_db()
    cur = conn.cursor()

    # ---------------- STUDENT INFO ----------------
    cur.execute("""
        SELECT enrollment_no, student_name, program, batch
        FROM students
        WHERE enrollment_no = ?
    """, (enrollment_no,))
    student = cur.fetchone()



    # Result declaration date
    cur.execute("""
        SELECT declared_date
        FROM results
        WHERE enrollment_no = ?
        ORDER BY declared_date DESC
        LIMIT 1
    """, (enrollment_no,))

    declared_date_row = cur.fetchone()
    declared_date = declared_date_row[0] if declared_date_row else None


    # ---------------- STUDENT RESULTS ----------------
    cur.execute("""
    SELECT semester,
           paper_code,
           subject_name,
           internal_marks,
           external_marks,
           total_marks,
           declared_date
    FROM results
    WHERE rowid IN (
        SELECT MAX(rowid)
        FROM results
        WHERE enrollment_no = ?
        GROUP BY paper_code
    )
    ORDER BY semester, paper_code
""", (enrollment_no,))

    results = cur.fetchall()

    # ---------------- NO RESULT CASE ----------------
    if not results:
        conn.close()
        return render_template(
            "student_dashboard.html",
            title="Student Dashboard",
            student=student,
            results=[],
            sgpa=0,
            percentage=0,
            subjects=0,
            highest=None,
            lowest=None,
            grades={
                "O": 0,
                "A+": 0,
                "A": 0,
                "B+": 0,
                "B": 0,
                "C": 0,
                "P": 0,
                "F": 0
            },
            passed=False,
            error="Result not uploaded yet"
        )

    # ---------------- CREDIT SYSTEM ----------------
    credits = {
        "MCA101": 4,
        "MCA103": 3,
        "MCA105": 3,
        "MCA107": 3,
        "MCA109": 3,
        "MCA161": 1,
        "MCA163": 1,
        "MCA165": 1,
        "MCA167": 1,
        "MCA169": 3,
        "MCA171": 1
    }

    # ---------------- INITIAL VALUES ----------------
    total_credit_points = 0
    total_credits = 0
    total_marks = 0

    grade_distribution = {
        "O": 0,
        "A+": 0,
        "A": 0,
        "B+": 0,
        "B": 0,
        "C": 0,
        "P": 0,
        "F": 0
    }

    highest = None
    lowest = None

    # ---------------- GRADE FUNCTION ----------------
    def grade_point(marks):
        if marks >= 90:
            return 10, "O"
        elif marks >= 75:
            return 9, "A+"
        elif marks >= 65:
            return 8, "A"
        elif marks >= 55:
            return 7, "B+"
        elif marks >= 50:
            return 6, "B"
        elif marks >= 45:
            return 5, "C"
        elif marks >= 40:
            return 4, "P"
        else:
            return 0, "F"

    # ---------------- CALCULATIONS ----------------
    for r in results:
        code = r[1].replace("-", "").strip()
        marks = float(r[5])

        credit = credits.get(code, 3)

        gp, grade = grade_point(marks)

        grade_distribution[grade] += 1
        total_credit_points += gp * credit
        total_credits += credit
        total_marks += marks

        if highest is None or marks > highest[1]:
            highest = (r[2], marks)

        if lowest is None or marks < lowest[1]:
            lowest = (r[2], marks)

    # ---------------- FINAL CALCULATIONS ----------------
    sgpa = round(total_credit_points / total_credits, 2) if total_credits > 0 else 0
    percentage = round(total_marks / len(results), 2) if len(results) > 0 else 0
    passed = all(float(r[5]) >= 40 for r in results)

    conn.close()

    # ---------------- RENDER TEMPLATE ----------------
    return render_template(
    "student_dashboard.html",
    title="Student Dashboard",
    student=student,
    results=results,
    sgpa=sgpa,
    percentage=percentage,
    subjects=len(results),
    highest=highest,
    lowest=lowest,
    grades=grade_distribution,
    passed=passed,
    declared_date=declared_date
)