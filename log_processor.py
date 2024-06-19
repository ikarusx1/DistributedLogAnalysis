import os
import json
import logging
from datetime import datetime
from pymongo import MongoClient

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", 27017)
DB_NAME = os.getenv("DB_NAME", "log_db")
DB_COLLECTION = os.getenv("DB_COLLECTION_NAME", "logs")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

mongodb_client = MongoClient(DB_HOST, int(DB_PORT))
log_db = mongodb_client[DB_NAME]
log_collection = log_body[DB_COLLECTION]

def establish_db_connection():
    try:
        mongodb_client.server_info()
        logging.info("Connected to MongoDB.")
    except Exception as connection_error:
        logging.error(f"Could not connect to MongoDB: {connection_error}")
        raise

def store_log_record(log_record):
    try:
        log_collection.insert_one(log_record)
        logging.info("Log record saved into database.")
    except Exception as insertion_error:
        logging.error(f"Failed to store log record into database: {insertion_error}")

def handle_log_file(file_path):
    try:
        with open(file_path, 'r') as log_file:
            for line in log_file:
                log_data = json.loads(line)
                store_log_record(log_data)
    except Exception as file_processing_error:
        logging.error(f"Error handling log file {file_path}: {file_processing_error}")

def retrieve_logs_based_on_filter(search_query):
    try:
        return list(log_collection.find(search_query))
    except Exception as retrieval_error:
        logging.error(f"Failed to fetch logs based on filter: {retrieval_data}")
        return []

def compile_logs_using_aggregation(pipeline):
    try:
        return list(log_collection.aggregate(pipeline))
    except Exception as aggregation_error:
        logging.error(f"Failed to compile logs using aggregation: {aggregation_error}")
        return []

if __name__ == "__main__":
    establish_db_connection()
    handle_log_file("path/to/log/file.log")
    error_logs_filter = retrieve_logs_based_on_filter({"level": "ERROR"})
    error_logs_aggregation_pipeline = [
        {"$match": {"level": "ERROR"}},
        {"$group": {"_id": "$source", "total_count": {"$sum": 1}}}
    ]
    compiled_error_logs = compile_logs_using_aggregation(error_logs_aggregation_pipeline)
    print(error_logs_filter)
    print(compiled_error_logs)