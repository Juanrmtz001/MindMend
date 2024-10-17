# app/self_care/routes.py
from fastapi import APIRouter
from app.self_care.models import SelfCareTool
from motor.motor_asyncio import AsyncIOMotorClient

self_care_router = APIRouter()

client = AsyncIOMotorClient(os.getenv("MONGODB_URI"))
db = client.mindmend

# List of self-care tools
@self_care_router.get("/", response_model=list)
async def get_self_care_tools():
    tools = await db.self_care_tools.find().to_list(100)
    return tools
