# Academic Result Analysis & Performance Dashboard

A web-based system designed to **manage, analyze, and visualize student academic performance** with role-based access for Admin, Faculty, and Students.

Website live link https://result-analysis-bwr7.onrender.com
---

## Overview

Traditional result systems only display marks without providing meaningful insights.
This project transforms raw academic data into **actionable analytics**, helping institutions and students understand performance trends, rankings, and subject-level insights.

---

## Objectives

* Automate result management
* Provide **SGPA-based performance analysis**
* Enable **data-driven academic insights**
* Reduce manual effort and errors in student management

---

## Features

###  Role-Based Access

* **Admin:** Upload results, manage users, view analytics
* **Faculty:** View subject-wise student performance
* **Student:** View personal results, SGPA, and charts

---

### CSV-Based Data Import

* Upload `results.csv` to store academic data
* Upload `students.csv` to create student accounts

---

### Automatic Student Account Creation

* No manual registration required
* Username = Enrollment Number
* Password = First Name

---

### SGPA Calculation System

* Credit-based evaluation (not just percentage)
* Grade classification (O, A+, A, B+, etc.)

---

### Student Ranking System

* Ranking based on SGPA
* Identifies top performers and weak students

---

### Performance Analytics Dashboard

* SGPA, percentage, subject-wise analysis
* Internal vs External comparison
* Top & weakest subjects

---

### Data Visualization

* Charts using Chart.js:

  * Marks distribution
  * Performance trends
  * Subject comparison

---

### Multi-Course Support

Supports multiple programs:

* MCA
* MBA
* BCA
* BBA

---

## System Workflow

1. Admin uploads CSV data
2. Data stored in SQLite database
3. System processes marks → calculates SGPA
4. Dashboards generate insights dynamically
5. Users access data based on roles

---

## Tech Stack

* **Backend:** Flask (Python)
* **Frontend:** HTML, CSS, JavaScript
* **Database:** SQLite
* **Templating Engine:** Jinja2
* **Charts & Visualization:** Chart.js

---

## Security Features

* Parameterized SQL queries (prevents SQL Injection)
* Session-based authentication
* Password hashing using Werkzeug

---

## Project Structure

```
project/
│── app.py
│── config.py
│
├── models/
│   └── db.py
│
├── routes/
│   ├── auth_routes.py
│   ├── admin_routes.py
│   ├── student_routes.py
│   └── faculty_routes.py
│
├── utils/
│   ├── csv_importer.py
│   ├── report_generator.py
│   └── file_utils.py
│
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── admin_dashboard.html
│   ├── student_dashboard.html
│   ├── faculty_dashboard.html
│   └── ...
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
└── uploads/
```

---

## Installation & Setup

### 1️ Clone Repository

```bash
git clone https://github.com/sarvesh1510/result-analysis.git
cd result-analysis
```

### 2️ Create Virtual Environment

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
```

### 3️ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️ Run Application

```bash
python app.py
```

### 5️ Open in Browser

```
http://127.0.0.1:5000
```

---

## Sample CSV Format

### students.csv

```
enrollment_no,student_name,program,batch
04450404425,Student name,MASTER OF COMPUTER APPLICATIONS,2025
```

### results.csv

```
enrollment_no,semester,paper_code,subject_name,internal_marks,external_marks,total_marks,exam_month_year,declared_date
01234567891,1,MCA101,DISCRETE STRUCTURES,30,40,70,12-2025,2026-01-22
```

---

## Unique Features

* No student registration required (CSV-based account creation)
* SGPA-based intelligent ranking system
* Real-time analytics dashboard
* Multi-course support
* Role-based architecture
* Modern UI design

---

## Future Scope

* Export reports in PDF/Excel
* AI-based performance prediction
* Email/SMS notifications
* Advanced role management

---

## Conclusion

This project simplifies academic result management by combining **automation, analytics, and visualization**, making it a practical solution for educational institutions.

---


If you like this project, give it a ⭐ on GitHub!
