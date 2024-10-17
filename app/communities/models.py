# app/communities/models.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CommunityPost(BaseModel):
    user_id: Optional[str]
    content: str
    timestamp: datetime = datetime.utcnow()
    community_id: str
