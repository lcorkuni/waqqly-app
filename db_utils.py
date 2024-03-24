import os
from enum import Enum

from pymongo import MongoClient
from log_conf import logger

DB_CONNECTION_STRING = os.getenv('DB_CONNECTION_STRING')

logger.info("Connecting to MongoDB...")
try:
    client = MongoClient(DB_CONNECTION_STRING)
except Exception as e:
    logger.error(f"ERROR: Connection to database failed: {e}")
logger.info("Successfully connected to MongoDB")

db = client["waqqly-database"]
users = db["users"]
dogs = db["dogs"]
walkers = db["walkers"]


class UserType(str, Enum):
    walker = "Dog Walker"
    owner = "Dog Owner"
    admin = "admin"


def insert_user(user_data: dict) -> None:
    user = {
        "username": user_data["username"],
        "email": user_data["email"],
        "hashed_password": user_data["password"],
        "type": user_data["userType"]
    }
    user_id = users.insert_one(user).inserted_id

    if user["type"] == UserType.owner:
        for dog in user_data["details"]["dogs"]:
            dog_to_insert = {
                "owner_id": user_id,
                "name": dog["name"],
                "breed": dog["breed"],
                "age": dog["age"]
            }
            dogs.insert_one(dog_to_insert)

    elif user["type"] == UserType.walker:
        walker = {
            "user_id": user_id,
            "first_name": user_data["details"]["firstName"],
            "last_name": user_data["details"]["lastName"],
            "age": user_data["details"]["age"]
        }
        walkers.insert_one(walker)
    logger.info(f"User {user['username']} successfully registered")