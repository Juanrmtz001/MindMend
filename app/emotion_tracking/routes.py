# app/emotion_tracking/routes.py
from fastapi import APIRouter, Depends
from app.auth.jwt_handler import get_current_user
from app.emotion_tracking.models import EmotionLog
from motor.motor_asyncio import AsyncIOMotorClient

emotion_router = APIRouter()

client = AsyncIOMotorClient(os.getenv("MONGODB_URI"))
db = client.mindmend

@emotion_router.post("/")
async def log_emotion(emotion: EmotionLog, current_user: dict = Depends(get_current_user)):
    emotion.user_id = current_user["_id"]
    await db.emotion_logs.insert_one(emotion.dict())
    return {"message": "Emotion logged successfully"}

@emotion_router.get("/", response_model=list)
async def get_emotions(current_user: dict = Depends(get_current_user)):
    emotions = await db.emotion_logs.find({"user_id": current_user["_id"]}).to_list(100)
    return emotions
