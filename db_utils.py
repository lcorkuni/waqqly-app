import os
import sys

from pymongo import MongoClient
from log_conf import logger

DB_CONNECTION_STRING = os.getenv('DB_CONNECTION_STRING')

logger.info("Connecting to MongoDB...")
try:
    client = MongoClient(DB_CONNECTION_STRING)
except Exception as e:
    logger.error(f"FATAL: Connection to database failed: {e}")
    sys.exit()
logger.info("Successfully connected to MongoDB")

db = client["waqqly-database"]
users = db["users"]
