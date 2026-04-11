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

@app.route("/")
def home():
    # Always open login page first
    return redirect(url_for("auth.login"))

if __name__ == "__main__":
    app.run(debug=True)
