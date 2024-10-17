# app/emotion_tracking/models.py
from pydantic import BaseModel, Field
from datetime import datetime

class EmotionLog(BaseModel):
    user_id: str
    date: datetime
    mood: int = Field(..., ge=1, le=10)
    stress: int = Field(..., ge=1, le=10)
