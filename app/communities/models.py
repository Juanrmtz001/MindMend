from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from bson import ObjectId


# Helper class to allow ObjectId in Pydantic models
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, field=None):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, *args, **kwargs):
        return {
            "type": "string",
            "format": "object-id"  # Customize the format if needed
        }

# Model for Community
class Community(BaseModel):
    # id: Optional[PyObjectId] = Field(alias="_id")  # Use _id for MongoDB compatibility
    name: str
    description: str
    members_count: int
    image_url: str = None
    type_of_mental_issue: List[str]

    class Config:
        populate_by_name = True  # Update the deprecated key
        json_encoders = {ObjectId: str}  # Convert ObjectId to string in JSON responses

# Model for Community Post
class CommunityPost(BaseModel):
    user_id: Optional[PyObjectId]  # Set as optional to allow anonymous posts
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)  # Default to current time
    community_id: PyObjectId  # Link to the community ObjectId

    class Config:
        json_encoders = {ObjectId: str}  # Convert ObjectId to string in JSON responses
