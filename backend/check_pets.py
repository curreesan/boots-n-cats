import asyncio
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.database import engine
from app.models.pet import Pet


async def check():
    async with AsyncSession(engine) as session:
        result = await session.exec(select(Pet))
        for p in result.all():
            print(p.id, p.name, p.breed)


asyncio.run(check())