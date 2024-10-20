from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.auth.routes import auth_router
from app.emotion_tracking.routes import emotion_router
from app.communities.routes import community_router
from app.professional_access.routes import professional_router
from app.self_care.routes import self_care_router

app = FastAPI()

# Mount the 'frontend' folder as a static directory for serving files
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Include routers for the backend API
app.include_router(auth_router, prefix="/auth")
app.include_router(emotion_router, prefix="/emotion-tracking")
app.include_router(community_router, prefix="/communities")
app.include_router(professional_router, prefix="/professional-access")
app.include_router(self_care_router, prefix="/self-care-tools")

# Serve the index.html on the home route
@app.get("/")
async def home():
    return {
        "message": "Welcome to the MindMend backend! Visit /static/index.html for the front-end."
    }
