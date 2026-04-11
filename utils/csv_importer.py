import csv
import sqlite3
from config import DATABASE_PATH
from werkzeug.security import generate_password_hash


# ---------------- IMPORT STUDENTS (USERS ONLY) ----------------
def import_students(csv_path):
    conn = sqlite3.connect(DATABASE_PATH)
    cur = conn.cursor()

    with open(csv_path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            enrollment = row["enrollment_no"].strip()
            name = row["student_name"].strip()

            # first name as password
            password = generate_password_hash(name.split()[0].lower())

            # Insert into students table
            cur.execute("""
                INSERT OR IGNORE INTO students
                (
                    enrollment_no,
                    student_name,
                    institute,
                    program,
                    batch,
                    year_of_admission
                )
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                enrollment,
                name,
                row["institute"].strip(),
                row["program"].strip(),
                row["batch"].strip(),
                row["year_of_admission"].strip()
            ))

            # Auto-create student login
            cur.execute("""
                INSERT OR IGNORE INTO users
                (username, password, role)
                VALUES (?, ?, ?)
            """, (
                enrollment,
                password,
                "student"
            ))

    conn.commit()
    conn.close()


# ---------------- IMPORT RESULTS (MARKS ONLY) ----------------
def import_results(csv_path):
    conn = sqlite3.connect(DATABASE_PATH)
    cur = conn.cursor()

    with open(csv_path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            enrollment_no = row["enrollment_no"].strip()
            semester = row["semester"].strip()
            paper_code = row["paper_code"].strip()

            # DELETE OLD RESULT FOR SAME STUDENT + SUBJECT + SEMESTER
            cur.execute("""
                DELETE FROM results
                WHERE enrollment_no = ?
                  AND semester = ?
                  AND paper_code = ?
            """, (
                enrollment_no,
                semester,
                paper_code
            ))

            # INSERT NEW LATEST RESULT
            cur.execute("""
                INSERT INTO results
                (
                    enrollment_no,
                    semester,
                    paper_code,
                    subject_name,
                    internal_marks,
                    external_marks,
                    total_marks,
                    exam_month_year,
                    declared_date
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                enrollment_no,
                semester,
                paper_code,
                row["subject_name"].strip(),
                row["internal_marks"].strip() if row["internal_marks"] else None,
                row["external_marks"].strip(),
                row["total_marks"].strip(),
                row["exam_month_year"].strip(),
                row["declared_date"].strip()
            ))

    conn.commit()
    conn.close()