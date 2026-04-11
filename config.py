import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
ALLOWED_EXTENSIONS = {"csv", "xlsx"}
DATABASE_PATH = os.path.join(BASE_DIR, "database", "db.sqlite3")
