import sqlite3
from config import DATABASE_PATH
from werkzeug.security import generate_password_hash

def get_db():
    return sqlite3.connect(DATABASE_PATH)

def init_db():
    conn = get_db()
    cur = conn.cursor()

    # USERS TABLE
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT
    )
    """)

    # STUDENTS TABLE
    cur.execute("""
    CREATE TABLE IF NOT EXISTS students (
        enrollment_no TEXT PRIMARY KEY,
        student_name TEXT,
        email TEXT,
        phone TEXT,
        institute TEXT,
        program TEXT,
        batch TEXT,
        year_of_admission TEXT
    )
    """)

    # RESULTS TABLE
    cur.execute("""
    CREATE TABLE IF NOT EXISTS results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        enrollment_no TEXT,
        semester INTEGER,
        paper_code TEXT,
        subject_name TEXT,
        internal_marks INTEGER,
        external_marks INTEGER,
        total_marks INTEGER,
        exam_month_year TEXT,
        declared_date TEXT,
        UNIQUE(enrollment_no, semester, paper_code)
    )
    """)

    # FACULTY SUBJECTS TABLE
    cur.execute("""
    CREATE TABLE IF NOT EXISTS faculty_subjects (
        username TEXT,
        program TEXT,
        semester INTEGER,
        paper_code TEXT,
        subject_name TEXT
    )
    """)

    # DEFAULT USERS (HASHED PASSWORDS)
    cur.execute("SELECT * FROM users")
    if not cur.fetchall():
        cur.execute(
            "INSERT INTO users VALUES (NULL, ?, ?, ?)",
            ("admin", generate_password_hash("admin123"), "admin")
        )
        cur.execute(
            "INSERT INTO users VALUES (NULL, ?, ?, ?)",
            ("faculty", generate_password_hash("faculty123"), "faculty")
        )
        cur.execute(
            "INSERT INTO users VALUES (NULL, ?, ?, ?)",
            ("student", generate_password_hash("student123"), "student")
        )

    conn.commit()
    conn.close()
