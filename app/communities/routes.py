# app/communities/routes.py
from fastapi import APIRouter, Depends, Query
from app.auth.jwt_handler import get_current_user
from app.communities.models import CommunityPost
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import os

community_router = APIRouter()

client = AsyncIOMotorClient(os.getenv("MONGODB_URI"))
db = client.mindmend

# Get communities route
@community_router.get("/")
async def get_communities(
    type_of_mental_issue: str = Query(None),  # Optional query parameter
    min_size: int = Query(None)  # Optional query parameter
):
    query = {}

    if type_of_mental_issue:
        query["type_of_mental_issue"] = type_of_mental_issue

    if min_size:
        query["size"] = {"$gte": min_size}

    # Retrieve communities based on query
    communities = await db.communities.find(query).to_list(100)
    return communities

# Post in a community route
@community_router.post("/")
async def post_in_community(post: CommunityPost, current_user: dict = Depends(get_current_user)):
    # Set the user_id if not anonymous
    if post.user_id is None:
        post.user_id = current_user["_id"]  # Use current user's ID

    # Insert the post into the community_posts collection
    await db.community_posts.insert_one(post.dict())
    return {"message": "Post created"}
