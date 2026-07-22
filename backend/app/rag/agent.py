import json

from openai import OpenAI
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.config import settings
from app.rag.tools import (
    tool_search_knowledge,
    tool_search_products,
    tool_search_pets,
    tool_create_consultation,
    TOOL_SCHEMAS,
)

client = OpenAI(base_url=settings.ollama_base_url, api_key="ollama")

SYSTEM_PROMPT = """
You are a helpful assistant for Boots and Cats, a pet store.
Answer questions about products, pets, and store policies using the tools
available to you. Always use search_knowledge for policy/care questions —
never answer those from memory. If a tool returns no relevant results,
say you don't have that information rather than guessing.

To submit an adoption consultation:
1. First call search_pets to find the pet's real id (a UUID). Never guess
   or invent a pet_id — it must come from a search_pets result.
2. You must have all three of: pet_id, contact, and preferred_time before
   offering to confirm. If the user hasn't given contact info or a
   preferred time, ASK for them explicitly — do not invent, guess, or use
   placeholder values like "your email" or "example.com" under any
   circumstances.
3. Once you have all three real values, respond with EXACTLY this format:
   "Confirm consultation request for [pet name] at [preferred time]? Reply YES to book."
4. Do not call create_consultation yet at this point — just ask.
5. Only when the user's next message is exactly "YES" (case-insensitive),
   call create_consultation using the exact values already collected.
"""


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
        response = client.chat.completions.create(
            model=settings.ollama_chat_model,
            messages=messages,
            tools=TOOL_SCHEMAS,
        )

        message = response.choices[0].message

        if not message.tool_calls:
            return message.content

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

    if name == "search_knowledge":
        return await tool_search_knowledge(args["query"])
    if name == "search_products":
        return await tool_search_products(args.get("species"), args.get("category"), session)
    if name == "search_pets":
        return await tool_search_pets(args.get("species"), session)
    if name == "create_consultation":
        return await tool_create_consultation(
            args["pet_id"], args["contact"], args["preferred_time"], user_id, session
        )

    return f"Unknown tool: {name}"