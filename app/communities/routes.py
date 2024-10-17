# app/communities/routes.py
from fastapi import APIRouter, Depends
from app.auth.jwt_handler import get_current_user
from app.communities.models import CommunityPost
from motor.motor_asyncio import AsyncIOMotorClient

community_router = APIRouter()

client = AsyncIOMotorClient(os.getenv("MONGODB_URI"))
db = client.mindmend

@community_router.get("/")
async def get_communities():
    communities = await db.communities.find().to_list(100)
    return communities

@community_router.post("/")
async def post_in_community(post: CommunityPost, current_user: dict = Depends(get_current_user)):
    if post.user_id is None:
        post.user_id = None  # Anonymous post
    await db.community_posts.insert_one(post.dict())
    return {"message": "Post created"}
