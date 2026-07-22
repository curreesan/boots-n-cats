import asyncio
from app.core.database import get_session
from app.models import user, pet, consultation  # ensures all tables are registered
from app.rag.agent import run_agent

TEST_USER_ID = "7843351e-2079-4de0-a5c8-4789078a06a3"


async def main():
    async for session in get_session():
        history = []

        answer1 = await run_agent(
            "I want to adopt Bruno, my number is 9876543210, call me evenings",
            session,
            TEST_USER_ID,
            history,
        )
        print("--- Turn 1 ---")
        print(answer1)

        history.append({"role": "user", "content": "I want to adopt Bruno, my number is 9876543210, call me evenings"})
        history.append({"role": "assistant", "content": answer1})

        answer2 = await run_agent("YES", session, TEST_USER_ID, history)
        print("--- Turn 2 ---")
        print(answer2)

        break


asyncio.run(main())