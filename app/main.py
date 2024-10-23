from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from app.auth.routes import auth_router
from app.emotion_tracking.routes import emotion_router
from app.communities.routes import community_router
from app.professional_access.routes import professional_router
from app.self_care.routes import self_care_router
import os

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
@app.get("/", response_class=HTMLResponse)
async def home():
    # Adjust the path to go one folder back and serve index.html
    index_path = os.path.join(os.path.dirname(__file__), "..", "index.html")
    with open(index_path) as f:
        return f.read()

# Serve the communities page
@app.get("/communities", response_class=HTMLResponse)
async def get_communities_page():
    with open("frontend/communities.html") as f:
        return f.read()