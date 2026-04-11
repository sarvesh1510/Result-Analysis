from flask import Blueprint, render_template, session, redirect, url_for, request
from werkzeug.utils import secure_filename
from utils.report_generator import generate_performance_report
import os
import sqlite3

from models.db import get_db
from config import UPLOAD_FOLDER
from utils.file_utils import allowed_file, read_file, validate_results_csv
from utils.csv_importer import import_students, import_results
from utils.report_generator import generate_academic_overview

admin_bp = Blueprint("admin", __name__)

# ---------------- ADMIN DASHBOARD ----------------
@admin_bp.route("/admin")
def admin_dashboard():
    if "user" not in session or session.get("role") != "admin":
        return redirect(url_for("auth.login"))

    return render_template("admin_dashboard.html", title="Admin Dashboard")


# ---------------- UPLOAD RESULTS (MARKS ONLY) ----------------
@admin_bp.route("/admin/upload", methods=["GET", "POST"])
def upload_results():
    if "user" not in session or session.get("role") != "admin":
        return redirect(url_for("auth.login"))

    message = None
    error = None

    if request.method == "POST":
        if "result_file" not in request.files:
            error = "No file selected"
        else:
            file = request.files["result_file"]

            if file.filename == "":
                error = "No file selected"

            elif not allowed_file(file.filename):
                error = "Only CSV or Excel files are allowed"

            else:
                filename = secure_filename(file.filename)
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                file.save(filepath)

                try:
                    df = read_file(filepath)

                    # ONLY results.csv is allowed
                    if filename.lower() != "results.csv":
                        error = "Please upload results.csv only"

                    elif not validate_results_csv(df):
                        error = "Invalid results CSV format"

                    else:
                        import_results(filepath)
                        message = "Results uploaded successfully"

                except Exception as e:
                    error = "Error processing file"

    return render_template(
        "upload_results.html",
        title="Upload Results",
        message=message,
        error=error
    )


# ---------------- MANAGE USERS ----------------
@admin_bp.route("/admin/users")
def manage_users():
    if "user" not in session or session.get("role") != "admin":
        return redirect(url_for("auth.login"))

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT username, role FROM users ORDER BY role")
    users = cur.fetchall()
    conn.close()

    return render_template(
        "manage_users.html",
        title="Manage Users",
        users=users
    )


# ---------------- IMPORT STUDENTS (USERS ONLY) ----------------
@admin_bp.route("/admin/import-students")
def import_students_csv():
    if "user" not in session or session.get("role") != "admin":
        return redirect(url_for("auth.login"))

    students_csv = os.path.join(UPLOAD_FOLDER, "students.csv")
    import_students(students_csv)

    return redirect(url_for("admin.manage_users", imported=1))

# ---------------- VIEW REPORTS ----------------
@admin_bp.route("/admin/reports")
def view_reports():
    if "user" not in session or session.get("role") != "admin":
        return redirect(url_for("auth.login"))

    course = request.args.get("course", "ALL")
    report = generate_performance_report(course)

    return render_template(
       "view_reports.html",
       report=report,
       selected_course=course
)

from flask import Response
import csv
from io import StringIO


@admin_bp.route("/admin/reports/export")
def export_reports():
    if "user" not in session or session.get("role") != "admin":
        return redirect(url_for("auth.login"))

    report = generate_performance_report()
    rows = report["rankings"]

    output = StringIO()
    writer = csv.writer(output)

    writer.writerow(["Enrollment No", "Average Marks"])

    for row in rows:
        writer.writerow(row)

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=performance_report.csv"
        }
    )

@admin_bp.route("/admin/academic-overview")
def academic_overview():
    if "user" not in session or session.get("role") != "admin":
        return redirect(url_for("auth.login"))

    course = request.args.get("course", "ALL")

    overview = generate_academic_overview(course)

    return render_template(
        "academic_overview.html",
        overview=overview,
        selected_course=course
    )