from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

# 📌 Database Initialization
DB_FILE = "users.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            tasbih_count INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

init_db()  # Initialize DB at start

# 📌 Signup Route
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username & Password required!"}), 400

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return jsonify({"message": "Signup Successful!"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Username already exists!"}), 409
    finally:
        conn.close()

# 📌 Login Route
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({"message": "Login Successful!", "username": username}), 200
    else:
        return jsonify({"error": "Invalid Credentials!"}), 401

# 📌 Save Tasbih Count
@app.route('/save_count', methods=['POST'])
def save_count():
    data = request.json
    username = data.get("username")
    count = data.get("count")

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET tasbih_count=? WHERE username=?", (count, username))
    conn.commit()
    conn.close()

    return jsonify({"message": "Tasbih Count Saved!"}), 200

# 📌 Get User Data
@app.route('/get_user/<username>', methods=['GET'])
def get_user(username):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT tasbih_count FROM users WHERE username=?", (username,))
    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({"username": username, "tasbih_count": user[0]}), 200
    else:
        return jsonify({"error": "User Not Found"}), 404

if __name__ == '__main__':
    app.run(debug=True)