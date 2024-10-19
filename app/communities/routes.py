# app/communities/routes.py
from fastapi import APIRouter, Depends
from app.auth.jwt_handler import get_current_user
from app.communities.models import CommunityPost
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import os

community_router = APIRouter()

client = AsyncIOMotorClient(os.getenv("MONGODB_URI"))
db = client.mindmend

@community_router.get("/")
async def get_communities():
    query = {}

    if type_of_mental_issue:
        query["type_of_mental_issue"] = type_of_mental_issue

    if min_size:
        query["size"] = {"$gte": min_size}

    communities = await db.communities.find(query).to_list(100)
    return communities

@community_router.post("/")
async def post_in_community(post: CommunityPost, current_user: dict = Depends(get_current_user)):
    if post.user_id is None:
        post.user_id = None  # Anonymous post
    await db.community_posts.insert_one(post.dict())
    return {"message": "Post created"}
