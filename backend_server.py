from flask import Flask
import os
from sqlalchemy import text

# Initialize Flask app
DATABASR_USER= os.getenv("DATABASE_USER", "appleuser")
DATABASR_PASS= os.getenv("DATABASE_PASS", "applepass")
DATABASR_HOST= os.getenv("DATABASE_HOST", "localhost")
DATABASR_PORT= os.getenv("DATABASE_PORT", "5432")
DATABASR_NAME= os.getenv("DATABASE_NAME", "appledb")
DATABASE_URL = f"postgresql://{DATABASR_USER}:{DATABASR_PASS}@{DATABASR_HOST}:{DATABASR_PORT}/{DATABASR_NAME}"
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["MAX_CONTENT_LENGTH"] = 600 * 1024 * 1024  # 600 MB limit

# Import db and initialize with app
from models.db import db

db.init_app(app)

# Import register_routes after app and db are initialized to avoid circular import
from routes.router import register_routes

register_routes(app)

if __name__ == "__main__":
    try:
        with app.app_context():
            db.create_all()
            db.session.execute(text("SELECT 1"))
        app.run(debug=True, host="0.0.0.0", port=8000)
    except Exception as e:
        print(f"Database connection failed: {e}")
        exit(1)
