import logging

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.database import engine
from app.core.security import decode_token
from app.rag.agent import run_agent
from app.rag.tools import tool_create_consultation
from app.routers.orders import perform_checkout

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

            if data.get("type") == "consultation_confirm":
                # The user submitted the real date picker triggered by
                # request_consultation — call tool_create_consultation
                # directly, bypassing the model entirely, so the stored
                # date is guaranteed to be the exact value the user picked
                # rather than anything the model could reword or invent.
                pet_id = data.get("pet_id", "")
                preferred_date = data.get("preferred_date", "")
                async with AsyncSession(engine) as session:
                    try:
                        answer = await tool_create_consultation(pet_id, preferred_date, user_id, session)
                    except Exception:
                        logger.exception("Consultation creation error for user %s", user_id)
                        answer = "Sorry, something went wrong submitting that request. Please try again."

                # Synthetic history entry so later turns in this conversation
                # have context that the booking happened.
                history.append({"role": "assistant", "content": answer})
                await websocket.send_json({"type": "answer", "content": answer})
                continue

            if data.get("type") == "checkout_place":
                # The user clicked the real "Confirm order" button
                # triggered by request_checkout — call perform_checkout
                # directly, bypassing the model entirely, same reasoning
                # as consultation_confirm above: an irreversible action
                # (decrements stock, creates a permanent order) should
                # never depend on the model correctly gating a text reply.
                import uuid as uuid_module

                async with AsyncSession(engine) as session:
                    try:
                        order = await perform_checkout(uuid_module.UUID(user_id), session)
                        answer = f"Order placed! Total: ₹{order.total_amount}."
                    except Exception as e:
                        logger.exception("Checkout error for user %s", user_id)
                        detail = getattr(e, "detail", "Something went wrong placing your order.")
                        answer = f"Sorry, checkout failed: {detail}"

                history.append({"role": "assistant", "content": answer})
                await websocket.send_json({"type": "answer", "content": answer, "cart_updated": True})
                continue

            user_message = data.get("content", "")

            async with AsyncSession(engine) as session:
                try:
                    result = await run_agent(user_message, session, user_id, history)
                except Exception:
                    logger.exception("Agent error for user %s", user_id)
                    result = {"type": "text", "content": "Sorry, I couldn't process your request at the moment. Please try again later."}

            history.append({"role": "user", "content": user_message})

            if result["type"] == "consultation_picker":
                # Not appended to history as a normal assistant text turn —
                # there's nothing textual the model "said" here, the picker
                # itself is the UI's response to this message.
                await websocket.send_json({
                    "type": "consultation_picker",
                    "pet_id": result["pet_id"],
                    "pet_name": result["pet_name"],
                })
            elif result["type"] == "checkout_confirm":
                await websocket.send_json({
                    "type": "checkout_confirm",
                    "item_count": result["item_count"],
                })
            else:
                history.append({"role": "assistant", "content": result["content"]})
                await websocket.send_json({
                    "type": "answer",
                    "content": result["content"],
                    "cart_updated": result.get("cart_updated", False),
                })

    except WebSocketDisconnect:
        pass