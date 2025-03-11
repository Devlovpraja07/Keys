from flask import Flask, render_template, request, redirect, url_for, jsonify
import os

app = Flask(__name__)

DATA_FILE = "data.txt"
USER_FILE = "users.txt"

# Function to save user data
def save_data(username, tasbih_count, image_path):
    with open(DATA_FILE, "a") as file:
        file.write(f"{username},{tasbih_count},{image_path}\n")

# Function to save new users
def save_user(username, password):
    with open(USER_FILE, "a") as file:
        file.write(f"{username},{password}\n")

# Function to check user login
def check_user(username, password):
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as file:
            users = file.readlines()
            for user in users:
                saved_username, saved_password = user.strip().split(",")
                if saved_username == username and saved_password == password:
                    return True
    return False

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/signup", methods=["POST"])
def signup():
    username = request.form.get("username")
    password = request.form.get("password")

    if username and password:
        save_user(username, password)
        return jsonify({"message": "Signup successful!"})

    return jsonify({"error": "Could not signup"})

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    if check_user(username, password):
        return jsonify({"message": "Login successful!"})

    return jsonify({"error": "Invalid login credentials"})

@app.route("/save", methods=["POST"])
def save():
    username = request.form.get("username")
    tasbih_count = request.form.get("tasbih_count")
    image_data = request.files.get("image")

    if username and tasbih_count and image_data:
        image_path = f"static/uploads/{username}.png"
        os.makedirs("static/uploads", exist_ok=True)
        image_data.save(image_path)

        save_data(username, tasbih_count, image_path)
        return jsonify({"message": "Data saved successfully!", "image": image_path})

    return jsonify({"error": "Invalid data!"})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")