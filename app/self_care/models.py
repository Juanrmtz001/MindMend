# app/self_care/models.py
from pydantic import BaseModel

class SelfCareTool(BaseModel):
    title: str
    description: str
    content_url: str
