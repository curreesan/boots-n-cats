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
    tool_create_consultation,
    TOOL_SCHEMAS,
)

client = AsyncOpenAI(base_url=settings.ollama_base_url, api_key="ollama")
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
) -> str:
    """
    Runs one full agent turn: sends the message + tool schemas to llama3.2,
    executes any requested tool calls, feeds results back, and returns the
    final text answer. Loops until the model stops requesting tools.
    """
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    if history:
        messages.extend(history)
    messages.append({"role": "user", "content": user_message})

    while True:
        response = await client.chat.completions.create(
            model=settings.ollama_chat_model,
            messages=messages,
            tools=TOOL_SCHEMAS,
            temperature=0.2,  # lower = more consistent tool-calling behavior, less improvisation
        )

        message = response.choices[0].message

        if not message.tool_calls:
            return _UUID_RE.sub("", message.content) if message.content else message.content

        messages.append({"role": "assistant", "content": message.content, "tool_calls": message.tool_calls})

        for tool_call in message.tool_calls:
            result = await _execute_tool(tool_call, session, user_id)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result,
            })


async def _execute_tool(tool_call, session: AsyncSession, user_id: str) -> str:
    """Dispatches a tool call to its actual Python function."""
    name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)
    logger.info("tool call: %s(%s)", name, args)

    if name == "search_knowledge":
        result = await tool_search_knowledge(args["query"])
    elif name == "search_products":
        result = await tool_search_products(args.get("species"), args.get("category"), session)
    elif name == "search_pets":
        result = await tool_search_pets(args.get("species"), session)
    elif name == "add_to_cart":
        result = await tool_add_to_cart(args["product_id"], args.get("quantity", 1), user_id, session)
    elif name == "create_consultation":
        result = await tool_create_consultation(
            args["pet_id"], args["contact"], args["preferred_time"], user_id, session
        )
    else:
        result = f"Unknown tool: {name}"

    logger.info("tool result: %s -> %s", name, result[:200])
    return result