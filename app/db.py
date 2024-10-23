# app/db.py
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from pymongo import MongoClient

# Connecting to MongoDB
cluster = "mongodb+srv://mindmend_user:mindmend_user@cluster0.s77ba.mongodb.net/mindmend_db?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(cluster)

# Fetching mindmend_db
db = client.mindmend_db

# # Load environment variables from a .env file
# load_dotenv()

# # MongoDB connection URI (this should be in your .env file)
# MONGODB_URI = os.getenv("MONGODB_URI")

# # Database name (optional, can be set in .env or default to 'mindmend_db')
# DB_NAME = os.getenv("DB_NAME", "mindmend_db")

# # Initialize MongoDB client
# client = AsyncIOMotorClient(MONGODB_URI)

# # Reference the database
# db = client[DB_NAME]
# print(f"Connecting to MongoDB at: {MONGODB_URI} with database: {DB_NAME}")