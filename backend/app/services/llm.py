# from backend.test_openai import OpenAI
from groq import Groq
from app.config import settings

# client = OpenAI(api_key=settings.OPENAI_API_KEY)
client = Groq(
    api_key=settings.GROQ_API_KEY
)

# def get_chat_response(message: str, system_prompt: str = None) -> str:
#     if not system_prompt:
#         system_prompt = "You are a helpful assistant."

#     response = client.chat.completions.create(
#         model="gpt-4o",
#         messages=[
#             {"role": "system", "content": system_prompt},
#             {"role": "user", "content": message}
#         ],
#         max_tokens=500
#     )

#     return response.choices[0].message.content

def get_chat_response(message: str):

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful AI assistant."
            },
            {
                "role": "user",
                "content": message
            }
        ]
    )

    return response.choices[0].message.content