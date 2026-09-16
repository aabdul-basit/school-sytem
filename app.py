from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import mysql.connector


app = Flask(__name__)
CORS(app)


# ==========================================
# MYSQL DATABASE CONNECTION
# ==========================================

def get_database():

    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="YOUR_MYSQL_PASSWORD",
        database="school_system"
    )


# ==========================================
# HOME PAGE
# ==========================================

@app.route("/")
def home():

    return render_template("home.html")


# ==========================================
# COURSES PAGE
# ==========================================

@app.route("/courses")
def courses():

    return render_template("courses.html")


# ==========================================
# APPLICATION FORM PAGE
# ==========================================

@app.route("/application")
def application():

    return render_template("apllicationform.html")


# ==========================================
# ADD STUDENT
# ==========================================

@app.route("/api/students", methods=["POST"])
def add_student():

    try:

        data = request.get_json()

        name = data.get("name")


        # Check name
        if not name or name.strip() == "":

            return jsonify({
                "success": False,
                "message": "Student name is required."
            }), 400


        name = name.strip()


        # Connect database
        db = get_database()

        cursor = db.cursor()


        # Insert student
        sql = """
            INSERT INTO students (name)
            VALUES (%s)
        """

        cursor.execute(sql, (name,))

        db.commit()


        # Get new student ID
        student_id = cursor.lastrowid


        cursor.close()
        db.close()


        return jsonify({

            "success": True,

            "message": "Student added successfully.",

            "student": {
                "id": student_id,
                "name": name
            }

        }), 201


    except Exception as error:

        print("ERROR:", error)

        return jsonify({

            "success": False,

            "message": "Database error."

        }), 500


# ==========================================
# GET ALL STUDENTS
# ==========================================

@app.route("/api/students", methods=["GET"])
def get_students():

    try:

        db = get_database()

        cursor = db.cursor(dictionary=True)


        cursor.execute("""
            SELECT id, name
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


    except Exception as error:

        print("ERROR:", error)

        return jsonify({

            "success": False,

            "message": "Database error."

        }), 500


# ==========================================
# TEST API
# ==========================================

@app.route("/api/test")
def test_api():

    return jsonify({

        "success": True,

        "message": "Flask backend is working!"

    })


# ==========================================
# START FLASK SERVER
# ==========================================

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )