from pydantic import BaseModel, EmailStr
from datetime import datetime
from bson import ObjectId

# Define the User schema (input for sign-up)
class User(BaseModel):
    id: str = None  # Adding an ID field for the user
    username: str
    password: str  # This will be hashed when saved in the database
    name: str
    email: EmailStr
    birthday: datetime  # Store birthday as a datetime

    class Config:
        # Convert ObjectId to string in JSON responses
        json_encoders = {ObjectId: str}

# Define how the user will be stored in the database (hashed password)
class UserInDB(User):
    hashed_password: str

    class Config:
        # Convert ObjectId to string in JSON responses
        json_encoders = {ObjectId: str}

# Define the EmotionTracking model
class EmotionTracking(BaseModel):
    mood: int  # Assuming mood is an integer rating
    stress: int  # Assuming stress is also an integer rating
