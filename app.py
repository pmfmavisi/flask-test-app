from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

# Create database if it doesn't exist
def init_db():
    if not os.path.exists("contact.db"):
        conn = sqlite3.connect("contact.db")
        c = conn.cursor()
        c.execute('''
            CREATE TABLE contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                message TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

@app.route("/")
def home():
    return redirect("/contact")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        conn = sqlite3.connect("contact.db")
        c = conn.cursor()
        c.execute("INSERT INTO contacts (name, email, message) VALUES (?, ?, ?)", (name, email, message))
        conn.commit()
        conn.close()

        return redirect("/thank-you")

    return render_template("contact.html")

@app.route("/thank-you")
def thank_you():
    return render_template("thank_you.html")


if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="0.0.0.0", port=5000)
