from pydantic import BaseModel, Field
from datetime import datetime
from bson import ObjectId

# Helper class to validate MongoDB ObjectIds
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, *args, **kwargs):
        return {
            "type": "string",
            "format": "object-id"  # Customize the format if needed
        }

# Model for logging emotions
class EmotionLog(BaseModel):
    user_id: str  # User ID will be passed explicitly
    mood: int = Field(..., ge=1, le=10)  # Mood should be between 1 and 10
    stress: int = Field(..., ge=1, le=10)  # Stress should be between 1 and 10
    date: datetime = Field(default_factory=datetime.utcnow)  # Default to current time
    user_name: str  # Add user name field

    class Config:
        json_encoders = {ObjectId: str}  # Convert ObjectId to string in JSON responses
        populate_by_name = True  # Update the deprecated key
