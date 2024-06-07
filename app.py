from flask import Flask, request, jsonify
import os
import sqlite3

app = Flask(__name__)

DATABASE_URL = os.getenv('DATABASE_URL', 'database.db')

def get_db_connection():
    conn = sqlite3.connect(DATABASE_URL)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/logs', methods=['GET'])
def fetch_logs():
    conn = get_db_connection()
    logs = conn.execute('SELECT * FROM logs').fetchall()
    conn.close()

    logs_list = [dict(log) for log in logs]
    return jsonify(logs_list)

@app.route('/logs', methods=['POST'])
def process_command():
    command_data = request.json

    command = command_data['command']
    data = command_data['data']

    conn = get_db_connection()
    conn.execute('INSERT INTO logs (command, data) VALUES (?, ?)', (command, data))
    conn.commit()
    conn.close()

    return jsonify({'status': 'success', 'message': 'Command processed and log added.'})

def initialize_database():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS logs (
                        id INTEGER PRIMARY KEY,
                        command TEXT NOT NULL,
                        data TEXT NOT NULL
                    )''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    initialize_database()
    app.run(debug=True, host='0.0.0.0', port=int(os.getenv('PORT', 5000)))