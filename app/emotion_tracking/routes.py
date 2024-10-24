from fastapi import APIRouter, Depends, HTTPException
from app.auth.jwt_handler import get_current_user
from app.emotion_tracking.models import EmotionLog
from app.db import db
from app.auth.models import User
from datetime import datetime

emotion_router = APIRouter()

# Route to get all logged emotions for the current user
@emotion_router.get("/")
async def get_emotions(current_user: dict = Depends(get_current_user)):
    # Query all emotions by user_id
    emotions = db.emotion_logs.find({"user_id": str(current_user["_id"])})
    
    # Convert the ObjectId to string in the returned data
    emotions_list = []
    for emotion in emotions:
        emotion["_id"] = str(emotion["_id"])
        emotions_list.append(emotion)
    
    return emotions_list

# Route to log emotions (POST request)
@emotion_router.post("/emotion_tracking")
async def log_emotion(emotion: EmotionLog, current_user: User = Depends(get_current_user)):  # User type hint
    print("Route hit, logging emotion")  # Add this to confirm route is hit
    
    emotion_dict = {
        "user_id": str(current_user["_id"]),
        "user_name": current_user.name,  # Assuming 'name' is an attribute in your User model
        "mood_level": emotion.mood_level,
        "stress_level": emotion.stress_level,
        "date": datetime.utcnow()  # Add current date for logging
    }
    
    print(f"Emotion Dict: {emotion_dict}")  # Check what gets inserted
    result = db.emotion_logs.insert_one(emotion_dict)
    
    if not result.inserted_id:
        raise HTTPException(status_code=500, detail="Failed to log emotion.")
    
    return {"message": "Emotion logged successfully", "id": str(result.inserted_id)}