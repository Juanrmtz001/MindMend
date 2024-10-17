# app/emotion_tracking/routes.py

from fastapi import APIRouter, Depends
from app.auth.jwt_handler import get_current_user
from app.emotion_tracking.models import EmotionLog
from app.db import db

emotion_router = APIRouter()

# Route to log emotions (protected)
@emotion_router.post("/")
async def log_emotion(emotion: EmotionLog, current_user: str = Depends(get_current_user)):
    emotion.user_id = current_user
    await db.emotion_logs.insert_one(emotion.dict())
    return {"message": "Emotion logged successfully"}

# Route to get logged emotions (protected)
@emotion_router.get("/")
async def get_emotions(current_user: str = Depends(get_current_user)):
    emotions = await db.emotion_logs.find({"user_id": current_user}).to_list(100)
    return emotions
