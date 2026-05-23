import nltk
from nltk.tokenize import word_tokenize

nltk.download('punkt')
import json
import sqlite3

from flask import Flask, render_template, request, jsonify, redirect, session

from chatbot_ai import get_response

app=Flask(__name__)
app.secret_key="mysecretkey"

# ==========================
# Database Creation
# ==========================

def create_db():

    conn = sqlite3.connect("users.db")

    c = conn.cursor()

    c.execute('''

    CREATE TABLE IF NOT EXISTS users(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    username TEXT,

    password TEXT

    )

    ''')

    conn.commit()

    conn.close()

create_db()


# ==========================
# Load chatbot data
# ==========================

with open("intents.json") as file:
    data=json.load(file)

def get_response(message):

    message=message.lower()

    for intent in data["intents"]:

        for pattern in intent["patterns"]:

            if pattern.lower() in message:

                return intent["responses"][0]

    return "Sorry, I couldn't understand."


# ==========================
# Chatbot Logic
# ==========================

def get_response(message):

    message = message.lower()

    for intent in data["intents"]:

        for pattern in intent["patterns"]:

            if pattern.lower() in message:

                return intent["responses"][0]

    return "Sorry, I couldn't understand."


# ==========================
# Home Page
# ==========================

@app.route("/")

def home():

    if "user" not in session:

        return redirect("/login")

    return render_template("index.html")


# ==========================
# Chat Route
# ==========================

@app.route("/get", methods=["POST"])

def chatbot():

    msg = request.form["msg"]

    return jsonify(
        {"reply": get_response(msg)}
    )


# ==========================
# Register Page
# ==========================

@app.route("/register", methods=["GET","POST"])

def register():

    if request.method == "POST":

        username = request.form["username"]

        password = request.form["password"]

        conn = sqlite3.connect("users.db")

        c = conn.cursor()

        c.execute(
            "INSERT INTO users(username,password) VALUES(?,?)",
            (username,password)
        )

        conn.commit()

        conn.close()

        return redirect("/login")

    return render_template("register.html")


# ==========================
# Login Page
# ==========================

@app.route("/login", methods=["GET","POST"])

def login():

    if request.method == "POST":

        username = request.form["username"]

        password = request.form["password"]

        conn = sqlite3.connect("users.db")

        c = conn.cursor()

        c.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username,password)
        )

        user = c.fetchone()

        conn.close()

        if user:

           session["user"]=username

           return redirect("/")

        else:

            return "Invalid Username or Password"

    return render_template("login.html")
@app.route("/logout")

def logout():

    session.pop("user",None)

    return redirect("/login")


# ==========================
# Run App
# ==========================

if __name__ == "__main__":

    app.run(debug=True)