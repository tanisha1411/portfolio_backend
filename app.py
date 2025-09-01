from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # allows frontend JS to call backend

# --- DB connection ---
def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT", 5432)
    )

# --- API route ---
@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    data = request.json

    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO messages
            (first_name, last_name, email, phone, message)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            data.get("firstName"),
            data.get("lastName"),
            data.get("email"),
            data.get("phone"),
            data.get("message")
        ))

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"status": "success"}), 200

    except Exception as e:
        print(e)
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/')
def home():
    return "Flask API is running."

if __name__ == '__main__':
    app.run(debug=True)
