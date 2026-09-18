import os

import mysql.connector
from mysql.connector import Error
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# ---------------------------------------------------------------------------
# MYSQL SETTINGS
# ---------------------------------------------------------------------------
# >>> PUT YOUR MYSQL PASSWORD HERE <<<
# Replace MY_MYSQL_PASSWORD (keep the quotes) with the password you chose when
# you installed MySQL Server.
#   - XAMPP users: the default password is empty, so use  ""
#   - Do not upload this file to GitHub with your real password inside it.
#
# Optional (safer): set an environment variable named MYSQL_PASSWORD and this
# code will use it automatically instead.
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": os.environ.get("MYSQL_PASSWORD", "MY_MYSQL_PASSWORD"),
    "database": "school_system",
    "charset": "utf8mb4",
}


def get_db_connection():
    """Open and return a new connection to the local MySQL server."""
    return mysql.connector.connect(**DB_CONFIG)


def db_error_response(err):
    """Print the MySQL error in the terminal and return a helpful JSON error.

    While you are developing, the message includes the real MySQL error so you
    can see it in the browser console. Before putting the site online, replace
    it with a generic message so you don't reveal database details.
    """
    code = getattr(err, "errno", None)
    detail = getattr(err, "msg", None) or str(err)

    if code == 1045:
        hint = ("Wrong MySQL username or password. "
                "Check the password in DB_CONFIG inside app.py.")
    elif code == 1049:
        hint = ("The database 'school_system' does not exist. "
                "Run database.sql first.")
    elif code == 1146:
        hint = ("The table 'students' does not exist. "
                "Run database.sql first.")
    elif code in (2002, 2003, 2005, 2006, 2013):
        hint = ("Cannot reach MySQL Server. "
                "Make sure the MySQL service is running.")
    else:
        hint = "Unexpected MySQL error."

    print(f"MySQL error {code}: {detail}")
    return jsonify(
        success=False,
        message=f"Database error: {hint} [MySQL error {code}: {detail}]",
    ), 500


# ---------------------------------------------------------------------------
# PAGE ROUTES
# ---------------------------------------------------------------------------
@app.route("/")
def home():
    return render_template("home.html")


@app.route("/courses")
def courses():
    return render_template("coursess.html")


@app.route("/application")
def application():
    return render_template("applicationform.html")


# ---------------------------------------------------------------------------
# API ROUTES
# ---------------------------------------------------------------------------
@app.route("/api/students", methods=["POST"])
def add_student():
    """Receive a student name as JSON and save it in MySQL."""
    data = request.get_json(silent=True) or {}
    name = data.get("name", "")

    # 1. Validate the name
    if not isinstance(name, str) or not name.strip():
        return jsonify(success=False, message="Student name is required."), 400

    name = name.strip()

    if len(name) > 100:
        return jsonify(
            success=False,
            message="Student name must be 100 characters or fewer.",
        ), 400

    # 2. Save it in MySQL
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # %s placeholders protect against SQL injection. Never build the
        # query by pasting the name directly into the SQL string.
        cursor.execute("INSERT INTO students (name) VALUES (%s)", (name,))
        connection.commit()

        new_id = cursor.lastrowid

        return jsonify(
            success=True,
            message="Student saved successfully.",
            student={"id": new_id, "name": name},
        ), 201

    except Error as err:
        return db_error_response(err)

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


@app.route("/api/students", methods=["GET"])
def get_students():
    """Return every saved student as JSON."""
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT id, name, created_at FROM students ORDER BY id")
        rows = cursor.fetchall()

        # JSON cannot store Python datetime objects, so convert to text.
        for row in rows:
            if row["created_at"] is not None:
                row["created_at"] = row["created_at"].strftime("%Y-%m-%d %H:%M:%S")

        return jsonify(success=True, count=len(rows), students=rows), 200

    except Error as err:
        return db_error_response(err)

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


if __name__ == "__main__":
    app.run(debug=True)