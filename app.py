from flask import Flask, redirect, url_for
from models.db import init_db

# Import all blueprints
from routes.auth_routes import auth_bp
from routes.admin_routes import admin_bp
from routes.faculty_routes import faculty_bp
from routes.student_routes import student_bp

app = Flask(__name__)
app.secret_key = "result_analysis_secret_key"

# Initialize database (creates tables + default users)
init_db()

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(faculty_bp)
app.register_blueprint(student_bp)

# Root route - still redirects to login
@app.route("/")
def home():
    return redirect(url_for("auth.login"))

# Health check route for Render
@app.route("/health")
def health():
    return "OK", 200

if __name__ == "__main__":
    # Production mode, disable debug
    app.run(debug=False)
