import logging

from fastapi import APIRouter, Depends
from sqlmodel import SQLModel, Field
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.database import get_session
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.rag.agent import run_agent

router = APIRouter(prefix="/chat", tags=["chat"])
logger = logging.getLogger(__name__)


class ChatMessage(SQLModel):
    content: str = Field(min_length=1)
    history: list[dict] = []


@router.post("")
async def chat(
    data: ChatMessage,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Plain HTTP wrapper around the agent — one request/response per message.
    No streaming, no persistence yet; the frontend must resend the full
    history each call (same idea as run_agent's own message list).

    Falls back to a friendly message on agent failure instead of a bare
    500, matching the websocket chat endpoint's behavior for the same
    failure mode. Doesn't support the consultation date-picker flow
    (that's websocket-only, see websocket_chat.py) — a picker signal
    here just surfaces as a plain informational answer instead.
    """
    user_id = str(user.id)
    try:
        result = await run_agent(data.content, session, user_id, data.history)
    except Exception:
        logger.exception("Agent error for user %s", user_id)
        result = {"type": "text", "content": "Sorry, I couldn't process your request at the moment. Please try again later."}

    if result["type"] == "consultation_picker":
        answer = f"To book a consultation for {result['pet_name']}, please use the chat widget on the site — it needs a date picker this endpoint doesn't support."
    elif result["type"] == "checkout_confirm":
        answer = "To place your order, please use the chat widget on the site — it needs a confirm button this endpoint doesn't support."
    else:
        answer = result["content"]
    return {"answer": answer}