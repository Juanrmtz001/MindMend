from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class EmotionLogCreate(BaseModel):
    mood: int = Field(..., ge=1, le=10)
    stress: int = Field(..., ge=1, le=10)

class EmotionLog(BaseModel):
    user_id: str
    user_name: str
    email: str
    mood: int = Field(..., ge=1, le=10)
    stress: int = Field(..., ge=1, le=10)
    date: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "mood": 7,
                "stress": 4
            }
        }