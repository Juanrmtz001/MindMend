# app/communities/models.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class Community(BaseModel):
    id: str
    name: str
    description: str
    num_of_members: int
    type_of_mental_issue: List[str]

class CommunityPost(BaseModel):
    user_id: Optional[str]
    content: str
    timestamp: datetime = datetime.utcnow()
    community_id: str