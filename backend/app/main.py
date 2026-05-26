from fastapi import FastAPI
from app.api.routes import chat

app = FastAPI(
    title="Avatar Platform API",
    version="0.1.0"
)

app.include_router(chat.router, prefix="/api/v1", tags=["chat"])

@app.get("/health")
def health_check():
    return {"status": "ok", "version": "0.1.0"}