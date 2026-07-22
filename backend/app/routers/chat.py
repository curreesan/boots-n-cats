from fastapi import APIRouter, Depends
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.database import get_session
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.rag.agent import run_agent

router = APIRouter(prefix="/chat", tags=["chat"])


class ChatMessage(SQLModel):
    content: str
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
    """
    answer = await run_agent(data.content, session, str(user.id), data.history)
    return {"answer": answer}