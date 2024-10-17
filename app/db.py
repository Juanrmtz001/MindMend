# app/db.py
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# MongoDB connection URI (this should be in your .env file)
MONGODB_URI = os.getenv("MONGODB_URI")

# Database name (optional, can be set in .env or default to 'mindmend_db')
DB_NAME = os.getenv("DB_NAME", "mindmend_db")

# Initialize MongoDB client
client = AsyncIOMotorClient(MONGODB_URI)

# Reference the database
db = client[DB_NAME]