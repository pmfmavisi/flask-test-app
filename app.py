from flask import Flask, render_template, request, redirect
from dotenv import load_dotenv
import os
import pyodbc

app = Flask(__name__)
load_dotenv()

# Azure SQL connection string
conn_str = os.getenv("AZURE_SQL_CONNECTION")

@app.route("/", methods=["GET"])
def home():
    return redirect("/contact")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        try:
            conn = pyodbc.connect(conn_str)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO contacts (name, email, message)
                VALUES (?, ?, ?)
            """, (name, email, message))
            conn.commit()
            conn.close()
        except Exception as e:
            return f"❌ Error saving to Azure SQL: {e}"

        return redirect("/thank-you")

    return render_template("contact.html")

@app.route("/thank-you")
def thank_you():
    return render_template("thank_you.html")

@app.route("/messages")
def messages():
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute("SELECT name, email, message FROM contacts")
        results = cursor.fetchall()
        conn.close()
    except Exception as e:
        return f"❌ Could not fetch messages: {e}"

    return render_template("messages.html", messages=results)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
