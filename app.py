from flask import Flask, render_template, request, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)


# =========================
# DATABASE CONNECTION
# =========================
def get_database():
    return mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="",
        database="school_system"
    )


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
    return render_template("coursess.html")


# =========================
# APPLICATION PAGE
# =========================
@app.route("/application")
def application():
    return render_template("applicationform.html")


# =========================
# TEST FLASK
# =========================
@app.route("/api/test")
def api_test():
    return jsonify({
        "success": True,
        "message": "Flask backend is working!"
    })


# =========================
# TEST DATABASE
# =========================
@app.route("/api/database-test")
def database_test():

    try:
        db = get_database()

        if db.is_connected():
            db.close()

            return jsonify({
                "success": True,
                "message": "Database connected successfully!"
            })

    except Error as error:

        print("Database error:", error)

        return jsonify({
            "success": False,
            "message": str(error)
        }), 500


# =========================
# SAVE STUDENT
# =========================
@app.route("/api/students", methods=["POST"])
def add_student():

    try:

        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "message": "No data received."
            }), 400

        name = data.get("name")

        if not name or name.strip() == "":
            return jsonify({
                "success": False,
                "message": "Student name is required."
            }), 400

        db = get_database()

        cursor = db.cursor()

        sql = """
        INSERT INTO students (name)
        VALUES (%s)
        """

        cursor.execute(sql, (name.strip(),))

        db.commit()

        student_id = cursor.lastrowid

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

    except Error as error:

        print("Database error:", error)

        return jsonify({
            "success": False,
            "message": "Database error: " + str(error)
        }), 500

    except Exception as error:

        print("Error:", error)

        return jsonify({
            "success": False,
            "message": str(error)
        }), 500


# =========================
# GET STUDENTS
# =========================
@app.route("/api/students", methods=["GET"])
def get_students():

    try:

        db = get_database()

        cursor = db.cursor(dictionary=True)

        cursor.execute("""
            SELECT id, name, created_at
            FROM students
            ORDER BY id DESC
        """)

        students = cursor.fetchall()

        cursor.close()
        db.close()

        return jsonify({
            "success": True,
            "students": students
        })

    except Error as error:

        print("Database error:", error)

        return jsonify({
            "success": False,
            "message": "Database error: " + str(error)
        }), 500


# =========================
# RUN FLASK
# =========================
if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )