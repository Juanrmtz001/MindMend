# app/communities/routes.py
from fastapi import APIRouter, Depends
from app.auth.jwt_handler import get_current_user
from app.communities.models import CommunityPost
from app.db import db
# from motor.motor_asyncio import AsyncIOMotorClient
# from bson import ObjectId
# import os

community_router = APIRouter()

# client = AsyncIOMotorClient(os.getenv("MONGODB_URI"))
# db = client.mindmend

# Get communities route
@community_router.get("/")
async def get_communities():
    # print("Fetching communities...")  # Debug log
    cursor = db.communities.find()
    communities = cursor.to_list(100)

    # Convert ObjectId to string for better readability
    communities = [
        {**community, "_id": str(community["_id"])} for community in communities
    ]
    
    print(f"Communities found: {communities}")  # Log the communities fetched
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
