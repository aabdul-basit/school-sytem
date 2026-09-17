from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)


# =========================
# DATABASE CONFIGURATION
# =========================

DATABASE = "school_system.db"


# =========================
# DATABASE CONNECTION
# =========================

def get_database():
    db = sqlite3.connect(DATABASE)

    # Allows rows to behave like dictionaries
    db.row_factory = sqlite3.Row

    return db


# =========================
# INITIALIZE DATABASE
# =========================

def init_database():
    db = get_database()

    cursor = db.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    db.commit()

    cursor.close()
    db.close()


# =========================
# HOME PAGE
# =========================

@app.route("/")
def home():
    return render_template("home.html")


# =========================
# COURSES PAGE
# =========================

@app.route("/courses")
def courses():
    return render_template("courses.html")


# =========================
# APPLICATION PAGE
# =========================

@app.route("/application")
def application():
    return render_template("applicationform.html")

# =========================
# DASHBOARD PAGE
# =========================

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


# =========================
# DASHBOARD API
# =========================

@app.route("/api/dashboard/students", methods=["GET"])
def dashboard_students():

    try:
        db = get_database()
        cursor = db.cursor()

        cursor.execute("""
            SELECT id, name, created_at
            FROM students
            ORDER BY id DESC
        """)

        rows = cursor.fetchall()

        students = [dict(row) for row in rows]

        cursor.close()
        db.close()

        return jsonify({
            "success": True,
            "students": students
        })

    except Exception as error:

        print("Dashboard database error:", error)

        return jsonify({
            "success": False,
            "message": "Could not load students."
        }), 500


# =========================
# SAVE STUDENT
# =========================

@app.route("/api/students", methods=["POST"])
def add_student():

    try:

        # Get data sent by JavaScript
        data = request.get_json()

        # Get student name
        name = data.get("name")

        # Check name
        if not name or name.strip() == "":
            return jsonify({
                "success": False,
                "message": "Student name is required."
            }), 400

        # Connect to SQLite
        db = get_database()

        cursor = db.cursor()

        # Insert student
        sql = """
            INSERT INTO students (name)
            VALUES (?)
        """

        cursor.execute(sql, (name.strip(),))

        # Save changes
        db.commit()

        # Get new student ID
        student_id = cursor.lastrowid

        # Close connection
        cursor.close()
        db.close()

        return jsonify({
            "success": True,
            "message": "Student saved successfully.",
            "student": {
                "id": student_id,
                "name": name.strip()
            }
        }), 201

    except Exception as error:

        print("Database error:", error)

        return jsonify({
            "success": False,
            "message": "Database error."
        }), 500


# =========================
# GET ALL STUDENTS
# =========================

@app.route("/api/students", methods=["GET"])
def get_students():

    try:

        # Connect to SQLite
        db = get_database()

        cursor = db.cursor()

        cursor.execute("""
            SELECT id, name, created_at
            FROM students
            ORDER BY id DESC
        """)

        rows = cursor.fetchall()

        # Convert SQLite rows to dictionaries
        students = [dict(row) for row in rows]

        cursor.close()
        db.close()

        return jsonify({
            "success": True,
            "students": students
        })

    except Exception as error:

        print("Database error:", error)

        return jsonify({
            "success": False,
            "message": "Database error."
        }), 500


# =========================
# TEST BACKEND
# =========================

@app.route("/api/test")
def test():

    return jsonify({
        "success": True,
        "message": "Flask backend is working!"
    })


# =========================
# RUN FLASK
# =========================

if __name__ == "__main__":

    # Create database and table
    init_database()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
