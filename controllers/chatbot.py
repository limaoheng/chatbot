from typing import Optional
from fastapi import APIRouter, HTTPException

from agents.ChatAgent import ChatAgent
from models.Message import Message

router = APIRouter()


@router.post("/chat")
async def chat(message: Message):
    try:
        chat = ChatAgent()
        res = chat.get_completion_from_messages(user_message=message.text, context=message.url)

        return {"response": res.strip()}
    except Exception as e:
        # Catch-all for other exceptions
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")
