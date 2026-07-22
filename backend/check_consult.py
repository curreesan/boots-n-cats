import asyncio
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.database import engine
from app.models.consultation import AdoptionConsultation


async def check():
    async with AsyncSession(engine) as session:
        result = await session.exec(select(AdoptionConsultation))
        for c in result.all():
            print(c.id, c.pet_id, c.contact, c.preferred_time, c.status)


asyncio.run(check())