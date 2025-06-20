from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sqlite3
from datetime import datetime

app = Flask(__name__, static_folder='../static', template_folder='../templates')
CORS(app)

# Setup SQLite DB
conn = sqlite3.connect('../database.db', check_same_thread=False)
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        message TEXT,
        time TEXT
    )
''')
conn.commit()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/send/<username>", methods=["POST"])
def send(username):
    data = request.get_json()
    msg = data.get("message", "").strip()
    if msg:
        timestamp = datetime.now().isoformat()
        c.execute("INSERT INTO messages (username, message, time) VALUES (?, ?, ?)", (username, msg, timestamp))
        conn.commit()
        return jsonify({"status": "success"})
    return jsonify({"status": "error", "msg": "Empty message"})

@app.route("/messages/<username>", methods=["GET"])
def get_messages(username):
    c.execute("SELECT message, time FROM messages WHERE username = ? ORDER BY id DESC", (username,))
    messages = [{"message": m, "time": t} for m, t in c.fetchall()]
    return jsonify(messages)

if __name__ == "__main__":
    app.run(debug=True)
