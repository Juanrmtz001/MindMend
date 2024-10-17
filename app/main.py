# app/main.py
from fastapi import FastAPI
from app.auth.routes import auth_router
from app.emotion_tracking.routes import emotion_router
from app.communities.routes import community_router
from app.professional_access.routes import professional_router
from app.self_care.routes import self_care_router

app = FastAPI()

# Include routers from different modules
app.include_router(auth_router, prefix="/auth")
app.include_router(emotion_router, prefix="/emotion-tracking")
app.include_router(community_router, prefix="/communities")
app.include_router(professional_router, prefix="/professional-access")
app.include_router(self_care_router, prefix="/self-care-tools")

# Home page route for testing
@app.get("/")
async def home():
    return {"message": "Welcome to MindMend!"}
