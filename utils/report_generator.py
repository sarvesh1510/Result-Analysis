from models.db import get_db


# ---------------- SAME GRADE FUNCTION AS STUDENT DASHBOARD ----------------
def grade_point(marks):
    if marks >= 90:
        return 10
    elif marks >= 75:
        return 9
    elif marks >= 65:
        return 8
    elif marks >= 55:
        return 7
    elif marks >= 50:
        return 6
    elif marks >= 45:
        return 5
    elif marks >= 40:
        return 4
    else:
        return 0


# ---------------- SAME CREDIT MAP ----------------
CREDITS = {
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


def generate_performance_report(course="ALL"):
    conn = get_db()
    cur = conn.cursor()

    # ---------------- COURSE FILTER ----------------
    if course == "ALL":
        cur.execute("""
            SELECT DISTINCT enrollment_no
            FROM results
            ORDER BY enrollment_no
        """)
    else:
        cur.execute("""
            SELECT DISTINCT r.enrollment_no
            FROM results r
            JOIN students s
            ON r.enrollment_no = s.enrollment_no
            WHERE s.program = ?
            ORDER BY r.enrollment_no
        """, (course,))

    students = [row[0] for row in cur.fetchall()]

    rankings = []
    passed_students = 0

    for enrollment_no in students:
        cur.execute("""
            SELECT semester, paper_code, subject_name,
                   internal_marks, external_marks, total_marks
            FROM results
            WHERE enrollment_no = ?
            GROUP BY semester, paper_code
            ORDER BY semester, paper_code
        """, (enrollment_no,))

        results = cur.fetchall()

        if not results:
            continue

        total_credit_points = 0
        total_credits = 0
        failed = False

        for r in results:
            code = r[1].replace("-", "").strip()
            marks = float(r[5])

            credit = CREDITS.get(code, 3)
            gp = grade_point(marks)

            total_credit_points += gp * credit
            total_credits += credit

            if marks < 40:
                failed = True

        sgpa = round(
            total_credit_points / total_credits, 2
        ) if total_credits > 0 else 0

        rankings.append((enrollment_no, sgpa))

        if not failed:
            passed_students += 1

    rankings.sort(key=lambda x: x[1], reverse=True)

    total_students = len(rankings)
    failed_students = total_students - passed_students

    avg_percentage = round(
        sum(row[1] for row in rankings) / total_students, 2
    ) if total_students > 0 else 0

    topper = rankings[0] if rankings else None

    conn.close()

    return {
        "total_students": total_students,
        "passed_students": passed_students,
        "failed_students": failed_students,
        "avg_percentage": avg_percentage,
        "topper": topper,
        "rankings": rankings
    }

def generate_academic_overview(course="ALL"):
    conn = get_db()
    cur = conn.cursor()

    # ---------------- COURSE FILTER (SAME AS REPORTS) ----------------
    if course == "ALL":
        cur.execute("""
            SELECT DISTINCT enrollment_no
            FROM results
            ORDER BY enrollment_no
        """)
    else:
        cur.execute("""
            SELECT DISTINCT r.enrollment_no
            FROM results r
            JOIN students s
            ON r.enrollment_no = s.enrollment_no
            WHERE s.program = ?
            ORDER BY r.enrollment_no
        """, (course,))

    students = [row[0] for row in cur.fetchall()]

    # ---------------- NO DATA ZERO STATE ----------------
    if not students:
        conn.close()
        return {
            "avg_sgpa": 0,
            "pass_percentage": 0,
            "failed_subjects": 0,
            "at_risk_count": 0,
            "semester_labels": [],
            "semester_values": [],
            "difficult_subjects": [],
            "top_performers": [],
            "at_risk_students": []
        }

    final_sgpas = []
    semester_totals = {}
    failed_subjects = 0

    # ---------------- STUDENT-WISE SGPA ----------------
    for enrollment_no in students:
        cur.execute("""
            SELECT semester, paper_code, subject_name, total_marks
            FROM results
            WHERE enrollment_no = ?
            GROUP BY semester, paper_code
            ORDER BY semester, paper_code
        """, (enrollment_no,))

        results = cur.fetchall()

        if not results:
            continue

        total_credit_points = 0
        total_credits = 0
        total_marks = 0
        total_subjects = 0

        for semester, paper_code, subject_name, total_marks_value in results:
            marks = float(total_marks_value)
            code = paper_code.replace("-", "").strip()

            credit = CREDITS.get(code, 3)
            gp = grade_point(marks)

            total_credit_points += gp * credit
            total_credits += credit
            total_marks += marks
            total_subjects += 1

            if semester not in semester_totals:
                semester_totals[semester] = []

            semester_totals[semester].append(gp)

            if marks < 40:
                failed_subjects += 1

        sgpa = round(
            total_credit_points / total_credits, 2
        ) if total_credits > 0 else 0

        percentage = round(
            total_marks / total_subjects, 2
        ) if total_subjects > 0 else 0

        final_sgpas.append((enrollment_no, sgpa, percentage))

    # ---------------- TOP 5 ----------------
    top_performers = sorted(
        final_sgpas,
        key=lambda x: (x[1], x[2]),
        reverse=True
    )[:5]

    # ---------------- AT RISK ----------------
    at_risk_students = sorted(
        [s for s in final_sgpas if s[1] < 6],
        key=lambda x: x[1]
    )[:5]

    # ---------------- KPIs ----------------
    avg_sgpa = round(
        sum([x[1] for x in final_sgpas]) / len(final_sgpas),
        2
    ) if final_sgpas else 0

    total_students = len(final_sgpas)
    passed_students = len([s for s in final_sgpas if s[1] >= 4])

    pass_percentage = round(
        (passed_students / total_students) * 100,
        2
    ) if total_students > 0 else 0

    # ---------------- DIFFICULT SUBJECTS ----------------
    difficult_subjects = []

    if final_sgpas:
        if course == "ALL":
            cur.execute("""
                SELECT subject_name, ROUND(AVG(total_marks), 2)
                FROM results
                GROUP BY subject_name
                ORDER BY AVG(total_marks) ASC
                LIMIT 5
            """)
        else:
            cur.execute("""
                SELECT r.subject_name, ROUND(AVG(r.total_marks), 2)
                FROM results r
                JOIN students s
                ON r.enrollment_no = s.enrollment_no
                WHERE s.program = ?
                GROUP BY r.subject_name
                ORDER BY AVG(r.total_marks) ASC
                LIMIT 5
            """, (course,))

        difficult_subjects = cur.fetchall()

    # ---------------- SEMESTER TREND ----------------
    semester_labels = []
    semester_values = []

    for sem in sorted(semester_totals.keys()):
        semester_labels.append(f"Sem {sem}")
        semester_values.append(
            round(
                sum(semester_totals[sem]) / len(semester_totals[sem]),
                2
            )
        )

    conn.close()

    return {
        "avg_sgpa": avg_sgpa,
        "pass_percentage": pass_percentage,
        "failed_subjects": failed_subjects,
        "at_risk_count": len(at_risk_students),
        "semester_labels": semester_labels,
        "semester_values": semester_values,
        "difficult_subjects": difficult_subjects,
        "top_performers": top_performers,
        "at_risk_students": at_risk_students
    }