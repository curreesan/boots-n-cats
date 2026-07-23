import logging

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.database import engine
from app.core.security import decode_token
from app.rag.agent import run_agent

router = APIRouter()
logger = logging.getLogger(__name__)


@router.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    """
    One persistent connection per browser tab. Auth happens once at
    connect time (via the same access_token cookie used everywhere else),
    not per message. Conversation history lives in memory for this
    connection only — lost if the connection drops (no persistence yet).
    """
    token = websocket.cookies.get("access_token")
    payload = decode_token(token) if token else None

    if not payload or payload.get("type") != "access":
        await websocket.close(code=4401)
        return

    await websocket.accept()
    user_id = payload["sub"]
    history: list[dict] = []

    try:
        while True:
            data = await websocket.receive_json()
            user_message = data.get("content", "")

            async with AsyncSession(engine) as session:
                try:
                    answer = await run_agent(user_message, session, user_id, history)
                except Exception:
                    logger.exception("Agent error for user %s", user_id)
                    answer = "Sorry, I couldn't process your request at the moment. Please try again later."

            history.append({"role": "user", "content": user_message})
            history.append({"role": "assistant", "content": answer})

            await websocket.send_json({"type": "answer", "content": answer})

    except WebSocketDisconnect:
        pass