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
    failure mode.
    """
    # Captured once, before run_agent — a tool call inside it (e.g.
    # create_consultation) may commit using this same request-scoped
    # session, which would expire user's attributes for any access after.
    user_id = str(user.id)
    try:
        answer = await run_agent(data.content, session, user_id, data.history)
    except Exception:
        logger.exception("Agent error for user %s", user_id)
        answer = "Sorry, I couldn't process your request at the moment. Please try again later."
    return {"answer": answer}