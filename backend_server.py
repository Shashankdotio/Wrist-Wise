from flask import Flask, send_from_directory
import os
from sqlalchemy import text

# Initialize Flask app
DATABASE_USER = os.getenv("DATABASE_USER", "appleuser")
DATABASE_PASS = os.getenv("DATABASE_PASS", "applepass")
DATABASE_HOST = os.getenv("DATABASE_HOST", "db")
DATABASE_PORT = os.getenv("DATABASE_PORT", "5432")
DATABASE_NAME = os.getenv("DATABASE_NAME", "appledb")
DATABASE_URL = f"postgresql://{DATABASE_USER}:{DATABASE_PASS}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
app = Flask(__name__, static_folder='frontend', static_url_path='')
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["MAX_CONTENT_LENGTH"] = 600 * 1024 * 1024  # 600 MB limit

# Import db and initialize with app
from models.db import db

db.init_app(app)

# Import register_routes after app and db are initialized to avoid circular import
from routes.router import register_routes

register_routes(app)

# Serve frontend
@app.route('/')
def serve_frontend():
    return send_from_directory('frontend', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('frontend', filename)

# Create database tables if they don't exist
with app.app_context():
    try:
        db.create_all()
        print("Database tables created successfully")
    except Exception as e:
        print(f"Error creating database tables: {e}")

if __name__ == "__main__":
    try:
        with app.app_context():
            db.create_all()
            db.session.execute(text("SELECT 1"))
        app.run(debug=True, host="0.0.0.0", port=8000)
    except Exception as e:
        print(f"Database connection failed: {e}")
        exit(1)
