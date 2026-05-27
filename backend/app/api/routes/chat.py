from fastapi import APIRouter, HTTPException
from app.models.avatar import ChatRequest, ChatResponse, ConversationHistory, Message
from app.services.llm import get_chat_response
from app.services.avatars import get_avatar

router = APIRouter()

# Store conversations in memory (will use DB later)
# Key: avatar_id, Value: ConversationHistory
active_conversations = {}

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat with an avatar with conversation history
    """
    try:
        # Get avatar
        avatar = get_avatar(request.avatar_id)
        if not avatar:
            raise HTTPException(status_code=404, detail="Avatar not found")

        # Get or create conversation
        if request.avatar_id not in active_conversations:
            active_conversations[request.avatar_id] = ConversationHistory(
                avatar_id=request.avatar_id
            )

        conversation = active_conversations[request.avatar_id]

        # Add user message to history
        conversation.add_message("user", request.message)

        # Get last 10 messages for context (so API doesn't get too long)
        context_messages = conversation.get_last_n_messages(10)

        # Get response from Groq
        response_text = get_chat_response(
            message=request.message,
            system_prompt=avatar.system_prompt,
            conversation_history=context_messages[:-1]  # Exclude the message we just added
        )

        # Add assistant response to history
        conversation.add_message("assistant", response_text)

        return ChatResponse(
            response=response_text,
            avatar_id=request.avatar_id,
            message_count=len(conversation.messages)
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/avatars")
async def list_avatars():
    """List all available avatars"""
    from app.services.avatars import list_avatars
    return {"avatars": list_avatars()}

@router.get("/conversation/{avatar_id}")
async def get_conversation(avatar_id: str):
    """Get conversation history for an avatar"""
    if avatar_id not in active_conversations:
        return {"messages": [], "avatar_id": avatar_id}

    return {
        "avatar_id": avatar_id,
        "messages": active_conversations[avatar_id].messages
    }

@router.delete("/conversation/{avatar_id}")
async def clear_conversation(avatar_id: str):
    """Clear conversation history for an avatar"""
    if avatar_id in active_conversations:
        del active_conversations[avatar_id]

    return {"status": "cleared", "avatar_id": avatar_id}