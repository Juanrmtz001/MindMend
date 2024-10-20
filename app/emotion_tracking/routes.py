from fastapi import APIRouter, Depends
from app.auth.jwt_handler import get_current_user
from app.emotion_tracking.models import EmotionLog
from app.db import db
from bson import ObjectId

emotion_router = APIRouter()

# Route to log emotions (POST request)
@emotion_router.post("/")
async def log_emotion(emotion: EmotionLog, current_user: dict = Depends(get_current_user)):
    emotion_dict = emotion.dict()
    
    # Store the ObjectId of the current user as a string
    emotion_dict["user_id"] = str(current_user["_id"])  # This line will work if user_id is removed from EmotionLog

    # Insert the emotion log into MongoDB
    await db.emotion_logs.insert_one(emotion_dict)
    return {"message": "Emotion logged successfully"}


# Route to get all logged emotions for the current user
@emotion_router.get("/")
async def get_emotions(current_user: dict = Depends(get_current_user)):
    # Query all emotions by user_id, ensuring it's stored as a string
    emotions = await db.emotion_logs.find({"user_id": str(current_user["_id"])}).to_list(100)
    
    # Convert ObjectId to string in the returned data (if necessary)
    for emotion in emotions:
        emotion["_id"] = str(emotion["_id"])
    
    return emotions
