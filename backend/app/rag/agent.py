import json
import logging
import re

from openai import AsyncOpenAI
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.config import settings
from app.rag.prompts import build_system_prompt
from app.rag.tools import (
    tool_search_knowledge,
    tool_search_products,
    tool_search_pets,
    tool_add_to_cart,
    tool_request_checkout,
    tool_request_consultation,
    TOOL_SCHEMAS,
)

client = AsyncOpenAI(base_url=settings.cloudflare_base_url, api_key=settings.cloudflare_api_token)
logger = logging.getLogger(__name__)

SYSTEM_PROMPT = build_system_prompt()

# Matches a raw UUID (e.g. from a tool's "id=..." output) that leaked into
# the model's final answer despite the prompt telling it not to show ids —
# small local models don't reliably follow that instruction, so this is a
# guaranteed backstop rather than relying on prompt compliance alone.
_UUID_RE = re.compile(r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b")


async def run_agent(
    user_message: str,
    session: AsyncSession,
    user_id: str,
    history: list[dict] | None = None,
) -> dict:
    """
    Runs one full agent turn: sends the message + tool schemas to the
    model, executes any requested tool calls, feeds results back, and
    returns the final result. Loops until the model stops requesting
    tools — EXCEPT for request_consultation, which ends the turn
    immediately (see below) rather than looping back to the model.

    Returns a dict instead of a plain string so the caller (websocket/
    REST chat routes) can tell a normal text answer apart from a
    "show the date picker" / "show the confirm-order button" signal, and
    also know whether the server-side cart changed this turn (the
    frontend's cart state lives in its own React context and has no
    other way of knowing add_to_cart ran):
      {"type": "text", "content": "...", "cart_updated": bool}
      {"type": "consultation_picker", "pet_id": "...", "pet_name": "..."}
      {"type": "checkout_confirm", "item_count": int}
    """
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    if history:
        messages.extend(history)
    messages.append({"role": "user", "content": user_message})

    cart_updated = False

    while True:
        response = await client.chat.completions.create(
            model=settings.cloudflare_chat_model,
            messages=messages,
            tools=TOOL_SCHEMAS,
            temperature=0.2,  # lower = more consistent tool-calling behavior, less improvisation
        )

        message = response.choices[0].message

        if not message.tool_calls:
            content = _UUID_RE.sub("", message.content) if message.content else message.content
            return {"type": "text", "content": content, "cart_updated": cart_updated}

        messages.append({
            "role": "assistant",
            "content": message.content or "",
            "tool_calls": [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments,
                    },
                }
                for tc in message.tool_calls
            ],
        })

        for tool_call in message.tool_calls:
            result = await _execute_tool(tool_call, session, user_id)

            if tool_call.function.name == "add_to_cart" and result.startswith("Added "):
                cart_updated = True

            # request_consultation's success path is a "SHOW_PICKER:id:name"
            # marker (see tools.py) — end the turn right here instead of
            # feeding it back to the model, since the model has nothing
            # useful left to do until the user actually submits the picker.
            if result.startswith("SHOW_PICKER:"):
                _, pet_id, pet_name = result.split(":", 2)
                return {"type": "consultation_picker", "pet_id": pet_id, "pet_name": pet_name}

            # request_checkout's success path is a "SHOW_CHECKOUT:count"
            # marker — same reasoning as SHOW_PICKER above: end the turn
            # here, don't let the model claim the order was placed before
            # the user has actually clicked Confirm in the UI.
            if result.startswith("SHOW_CHECKOUT:"):
                item_count = int(result.split(":", 1)[1])
                return {"type": "checkout_confirm", "item_count": item_count}

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result,
            })


async def _execute_tool(tool_call, session: AsyncSession, user_id: str) -> str:
    """Dispatches a tool call to its actual Python function."""
    name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)
    # granite occasionally double-encodes arguments (a JSON string that
    # itself decodes to another JSON string) — decode again if so.
    if isinstance(args, str):
        args = json.loads(args)
    logger.info("tool call: %s(%s)", name, args)

    if name == "search_knowledge":
        result = await tool_search_knowledge(args["query"])
    elif name == "search_products":
        result = await tool_search_products(args.get("species"), args.get("category"), session)
    elif name == "search_pets":
        result = await tool_search_pets(args.get("species"), session)
    elif name == "add_to_cart":
        result = await tool_add_to_cart(args["product_id"], args.get("quantity", 1), user_id, session)
    elif name == "request_checkout":
        result = await tool_request_checkout(user_id, session)
    elif name == "request_consultation":
        result = await tool_request_consultation(args["pet_id"], user_id, session)
    else:
        result = f"Unknown tool: {name}"

    logger.info("tool result: %s -> %s", name, result[:200])
    return result