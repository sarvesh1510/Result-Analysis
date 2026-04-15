from flask import Flask, redirect, url_for
from models.db import init_db

app = Flask(__name__)
app.secret_key = "result_analysis_secret_key"

# Register blueprints (your existing ones)
from routes.auth_routes import auth_bp
from routes.admin_routes import admin_bp
from routes.faculty_routes import faculty_bp
from routes.student_routes import student_bp

app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(faculty_bp)
app.register_blueprint(student_bp)

# Initialize database lazily after first request
@app.before_first_request
def initialize():
    init_db()

# Health check for Render
@app.route("/health")
def health():
    return "OK", 200

# Root route redirects to login
@app.route("/")
def home():
    return redirect(url_for("auth.login"))

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
