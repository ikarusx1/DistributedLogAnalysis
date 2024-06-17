import os
import json
import logging
from datetime import datetime
from pymongo import MongoClient

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", 27017)
DB_NAME = os.getenv("DB_NAME", "log_db")
DB_COLLECTION_NAME = os.getenv("DB_COLLECTION_NAME", "logs")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

client = MongoClient(DB_HOST, int(DB_PORT))
db = client[DB_NAME]
collection = db[DB_COLLECTION_NAME]

def connect_to_db():
    try:
        client.server_info()
        logging.info("Connected to MongoDB.")
    except Exception as e:
        logging.error(f"Could not connect to MongoDB: {e}")
        raise

def insert_log(log):
    try:
        collection.insert_one(log)
        logging.info("Log inserted into database.")
    except Exception as e:
        logging.error(f"Failed to insert log into database: {e}")

def process_log_file(file_path):
    try:
        with open(file_path, 'r') as file:
            for line in file:
                log_data = json.loads(line)
                insert_log(log_data)
    except Exception as e:
        logging.error(f"Error processing log file {file_path}: {e}")

def filter_logs(query):
    try:
        return list(collection.find(query))
    except Exception as e:
        logging.error(f"Failed to retrieve filtered logs: {e}")
        return []

def aggregate_logs(pipeline):
    try:
        return list(collection.aggregate(pipeline))
    except Exception as e:
        logging.error(f"Failed to aggregate logs: {e}")
        return []

if __name__ == "__main__":
    connect_to_db()
    process_log_file("path/to/log/file.log")
    filtered_logs = filter_logs({"level": "ERROR"})
    aggregation_pipeline = [
        {"$match": {"level": "ERROR"}},
        {"$group": {"_id": "$source", "count": {"$sum": 1}}}
    ]
    aggregated_logs = aggregate_logs(aggregation_pipeline)
    print(filtered_logs)
    print(aggregated_logs)