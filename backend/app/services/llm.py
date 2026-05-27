from groq import Groq
from app.config import settings
from app.models.avatar import Message

# Initialize Groq client
client = Groq(api_key=settings.GROQ_API_KEY)

def get_chat_response(
    message: str,
    system_prompt: str,
    conversation_history: list
) -> str:
    """
    Get response from Groq with conversation history

    Args:
        message: Current user message
        system_prompt: Avatar personality/system instructions
        conversation_history: List of previous Message objects

    Returns:
        Response text from Groq
    """

    # Build messages for API call
    messages = [
        {"role": "system", "content": system_prompt}
    ]

    # Add conversation history
    for msg in conversation_history:
        messages.append({
            "role": msg.role,
            "content": msg.content
        })

    # Add current message
    messages.append({
        "role": "user",
        "content": message
    })

    # Call Groq API
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",  # Free Groq model
        messages=messages,
        temperature=0.7,
        max_tokens=500
    )

    return response.choices[0].message.content