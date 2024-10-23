# app/professional_access/routes.py
import os
from fastapi import APIRouter, Depends
from app.auth.jwt_handler import get_current_user
from motor.motor_asyncio import AsyncIOMotorClient

professional_router = APIRouter()

client = AsyncIOMotorClient(os.getenv("MONGODB_URI"))
db = client.mindmend

@professional_router.get("/")
async def get_professional_access():
    therapists = await db.professionals.find().to_list(100)
    return therapists

@professional_router.post("/session")
async def schedule_session(session_data: dict, current_user: dict = Depends(get_current_user)):
    session_data['user_id'] = current_user["_id"]
    await db.sessions.insert_one(session_data)
    return {"message": "Session scheduled"}
