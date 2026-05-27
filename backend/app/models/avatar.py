from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Message(BaseModel):
    role: str  # "user" or "assistant"
    content: str
    timestamp: Optional[datetime] = None

class ConversationHistory(BaseModel):
    avatar_id: str
    messages: List[Message] = []

    def add_message(self, role: str, content: str):
        self.messages.append(
            Message(role=role, content=content, timestamp=datetime.now())
        )

    def get_last_n_messages(self, n: int = 10) -> List[Message]:
        """Get last N messages for context"""
        return self.messages[-n:] if len(self.messages) > n else self.messages

class AvatarPersona(BaseModel):
    avatar_id: str
    name: str
    system_prompt: str
    description: str
    voice_id: Optional[str] = None
    photo_url: Optional[str] = None

class ChatRequest(BaseModel):
    message: str
    avatar_id: str

class ChatResponse(BaseModel):
    response: str
    avatar_id: str
    message_count: int