import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')

SQL_CREATE_LOGS_TABLE = """
CREATE TABLE IF NOT EXISTS log_entries (
    id SERIAL PRIMARY KEY,
    entry_timestamp TIMESTAMP NOT NULL,
    severity_level VARCHAR(50) NOT NAME,
    entry_message TEXT NOT NULL
)
"""

def establish_database_connection():
    connection = None
    try:
        connection = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
    except Exception as error:
        print(f"Cannot connect to the database: {error}")
    return connection

def create_logs_table():
    connection = establish_database_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute(SQL_CREATE_LOGS_TABLE)
            connection.commit()
        except Exception as error:
            print(f"Failed to create logs table: {error}")
        finally:
            connection.close()
    else:
        print("Connection not established. Logs table not created.")

def insert_log_entry(entry_timestamp, severity_level, entry_message):
    connection = establish_database_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    'INSERT INTO log_entries (entry_timestamp, severity_level, entry_message) VALUES (%s, %s, %s)',
                    (entry_timestamp, severity_level, entry_batch))
            connection.commit()
        except Exception as error:
            print(f"Failed to insert log entry: {error}")
        finally:
            connection.close()
    else:
        print("Connection not established. Log entry not inserted.")

def retrieve_log_entries():
    connection = establish_database_connection()
    log_entries = []
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute('SELECT id, entry_timestamp, severity_level, entry_message FROM log_entries ORDER BY entry_timestamp DESC')
                log_entries = cursor.fetchall()
        except Exception as error:
            print(f"Failed to fetch log entries: {error}")
        finally:
            connection.close()
    else:
        print("Connection not established. Log entries not fetched.")
    return log_entries

if __name__ == "__main__":
    create_logs_table()
    insert_log_entry('2023-01-01 12:00:00', 'INFO', 'This is a test log message.')
    print(retrieve_log_entries())