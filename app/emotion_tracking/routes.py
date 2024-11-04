from fastapi import APIRouter, Depends, HTTPException
from app.auth.jwt_handler import get_current_user
from app.emotion_tracking.models import EmotionLog, EmotionLogCreate
from app.db import db
from datetime import datetime

emotion_router = APIRouter()

@emotion_router.post("/emotions")
async def log_emotion(emotion: EmotionLogCreate, current_user: dict = Depends(get_current_user)):
    try:
        emotion_dict = {
            "user_id": str(current_user["_id"]),
            "user_name": current_user.get("name", "Unknown"),
            "email": current_user["email"],
            "mood": emotion.mood,
            "stress": emotion.stress,
            "date": datetime.utcnow()
        }
        
        # Debug prints
        print(f"Received emotion data: {emotion}")
        print(f"Current user: {current_user}")
        print(f"Emotion dict to insert: {emotion_dict}")
        
        result = db.emotion_logs.insert_one(emotion_dict)
        if not result.inserted_id:
            raise HTTPException(status_code=500, detail="Failed to log emotion.")
        
        return {
            "message": "Emotion logged successfully",
            "id": str(result.inserted_id)
        }
    except Exception as e:
        print(f"Error logging emotion: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Error logging emotion: {str(e)}"
        )

@emotion_router.get("/emotions")
async def get_emotions(current_user: dict = Depends(get_current_user)):
    try:
        emotions = list(db.emotion_logs.find({"user_id": str(current_user["_id"])}))
        return [
            {
                "_id": str(emotion["_id"]),
                "mood": emotion["mood"],
                "stress": emotion["stress"],
                "date": emotion["date"],
                "user_name": emotion["user_name"],
                "email": emotion["email"]
            }
            for emotion in emotions
        ]
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving emotions: {str(e)}"
        )