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
    search_query = request.args.get('query', None)
    conn = get_db_connection()
    if search_query:
        logs = conn.execute('SELECT * FROM logs WHERE command LIKE ? OR data LIKE ?', ('%'+search_request+'%', '%'+search_request+'%')).fetchall()
    else:
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

@app.route('/logs/<int:log_id>', methods=['DELETE'])
def delete_log_by_id(log_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM logs WHERE id = ?', (logid,))
    conn.commit()
    conn.close()

    return jsonify({'status': 'success', 'message': f'Log with id {logid} has been deleted.'})

@app.route('/logs', methods=['DELETE'])
def delete_log_by_command():
    command = request.args.get('command')
    if not command:
        return jsonify({'status': 'failure', 'message': 'Command query parameter is required for deletion.'}), 400

    conn = get_db_connection()
    conn.execute('DELETE FROM logs WHERE command = ?', (command,))
    conn.commit()
    conn.close()

    return jsonify({'status': 'success', 'message': f'Logs with command "{command}" have been deleted.'})

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