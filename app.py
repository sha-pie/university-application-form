
from flask import Flask, render_template, request
import sqlite3
import json
from datetime import datetime
from pathlib import Path

app = Flask(__name__)

DATABASE = Path(__file__).resolve().parent / "applications.db"


def create_database():
    connection = sqlite3.connect(DATABASE)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            applicant_name TEXT,
            submitted_at TEXT,
            application_data TEXT
        )
    """)

    connection.commit()
    connection.close()


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        form_data = request.form.to_dict(flat=False)

        first_name = request.form.get("first_name", "")
        surname = request.form.get("surname", "")

        applicant_name = first_name + " " + surname

        submitted_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        connection = sqlite3.connect(DATABASE)

        connection.execute("""
            INSERT INTO applications
            (applicant_name, submitted_at, application_data)
            VALUES (?, ?, ?)
        """, (
            applicant_name,
            submitted_at,
            json.dumps(form_data, ensure_ascii=False)
        ))

        connection.commit()
        connection.close()

        return render_template("index.html", success=True)
    return render_template("index.html")


if __name__ == "__main__":
    create_database()
    app.run(debug=True)
