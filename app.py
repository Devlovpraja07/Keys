from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Database setup (local storage)
def init_db():
    conn = sqlite3.connect("tasbih.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS tasbih (id INTEGER PRIMARY KEY, count INTEGER)")
    conn.commit()
    conn.close()

@app.route('/save_count', methods=['POST'])
def save_count():
    data = request.json
    count = data.get("count", 0)

    conn = sqlite3.connect("tasbih.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasbih (count) VALUES (?)", (count,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Tasbih count saved!", "count": count})

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host="0.0.0.0")