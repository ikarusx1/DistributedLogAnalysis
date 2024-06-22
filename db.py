import os
import psycopg2
from psycopg2.extras import execute_batch
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')

CREATE_LOG_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS logs (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    log_level VARCHAR(50) NOT NULL,
    message TEXT NOT NULL
)
"""

def get_db_connection():
    conn = None
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
    except Exception as e:
        print(f"Cannot connect to database: {e}")
    return conn

def create_schema():
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute(CREATE_LOG_TABLE_SQL)
            conn.commit()
        except Exception as e:
            print(f"Failed to create schema: {e}")
        finally:
            conn.close()
    else:
        print("Connection not established. Schema not created.")

def insert_log(timestamp, log_level, message):
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute('INSERT INTO logs (timestamp, log_level, message) VALUES (%s, %s, %s)',
                               (timestamp, log_level, message))
            conn.commit()
        except Exception as e:
            print(f"Failed to insert log: {e}")
        finally:
            conn.close()
    else:
        print("Connection not established. Log not inserted.")

def fetch_logs():
    conn = get_db_connection()
    logs = []
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute('SELECT id, timestamp, log_level, message FROM logs ORDER BY timestamp DESC')
                logs = cursor.fetchall()
        except Exception as e:
            print(f"Failed to fetch logs: {e}")
        finally:
            conn.close()
    else:
        print("Connection not established. Logs not fetched.")
    return logs

if __name__ == "__main__":
    create_schema()
    insert_log('2023-01-01 12:00:00', 'INFO', 'This is a test log message.')
    print(fetch_logs())