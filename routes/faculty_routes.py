from flask import Blueprint, render_template, session, redirect, url_for
from models.db import get_db

faculty_bp = Blueprint("faculty", __name__)


@faculty_bp.route("/faculty")
def faculty_dashboard():
    if "user" not in session or session.get("role") != "faculty":
        return redirect(url_for("auth.login"))

    username = session.get("user")

    conn = get_db()
    cur = conn.cursor()

    # Assigned faculty subject
    cur.execute("""
        SELECT program, semester, paper_code, subject_name
        FROM faculty_subjects
        WHERE username = ?
    """, (username,))
    faculty_info = cur.fetchone()

    if not faculty_info:
        conn.close()
        return render_template(
            "faculty_dashboard.html",
            error="No subject assigned"
        )

    program, semester, paper_code, subject_name = faculty_info

    # Students in this program
    cur.execute("""
        SELECT enrollment_no, student_name
        FROM students
        WHERE program = ?
    """, (program,))
    students = cur.fetchall()

    # Results only for assigned subject
    cur.execute("""
        SELECT enrollment_no, total_marks
        FROM results
        WHERE paper_code = ?
    """, (paper_code,))
    marks = cur.fetchall()

    # Quick analytics
    total_students = len(students)
    total_results = len(marks)

    passed = len([m for m in marks if m[1] >= 40])
    failed = total_results - passed
    avg_marks = round(
        sum([m[1] for m in marks]) / total_results,
        2
    ) if total_results > 0 else 0

    weak_students = [m for m in marks if m[1] < 40]

    topper = max(marks, key=lambda x: x[1]) if marks else None

    conn.close()

    return render_template(
        "faculty_dashboard.html",
        faculty_info=faculty_info,
        students=students,
        marks=marks,
        total_students=total_students,
        total_results=total_results,
        passed=passed,
        failed=failed,
        avg_marks=avg_marks,
        weak_students=weak_students,
        topper=topper
    )