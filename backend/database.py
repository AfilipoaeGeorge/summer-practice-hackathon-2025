from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
MONGO_URI = "mongodb://localhost:27017"

client = MongoClient(MONGO_URI)
db = client["gitgud"]

users_collection = db["users"]
tasks_collection = db["tasks"]
suggestions_collection = db["suggestions"]
projects_collection = db["projects"]
comments_collection = db["comments"]
projects_update_collection = db["projects_update"]