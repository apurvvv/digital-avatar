from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    message: str
    avatar_id: Optional[str] = None  # we'll use this later

class ChatResponse(BaseModel):
    response: str
    avatar_id: Optional[str] = None