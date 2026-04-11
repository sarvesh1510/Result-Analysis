import os
import pandas as pd
from config import ALLOWED_EXTENSIONS


# ---------------- FILE TYPE CHECK ----------------
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# ---------------- READ CSV / EXCEL ----------------
def read_file(filepath):
    ext = filepath.rsplit(".", 1)[1].lower()

    if ext == "csv":
        return pd.read_csv(filepath)
    elif ext == "xlsx":
        return pd.read_excel(filepath)
    else:
        return None


# ---------------- DEMO / GENERIC VALIDATION ----------------
# (kept for backward compatibility or future demo files)
def validate_structure(df):
    required_columns = {"roll_no", "subject", "marks"}
    return required_columns.issubset(set(df.columns))


# ---------------- RESULTS CSV VALIDATION (REAL DATASET) ----------------
def validate_results_csv(df):
    required_columns = {
        "enrollment_no",
        "semester",
        "paper_code",
        "subject_name",
        "internal_marks",
        "external_marks",
        "total_marks",
        "exam_month_year",
        "declared_date"
    }

    return required_columns.issubset(set(df.columns))
