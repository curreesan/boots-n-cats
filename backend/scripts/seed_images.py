"""
Backfills image_url for every existing product and pet with a stable
placeholder from picsum.photos, seeded by each row's own id so the same
item always gets the same image and the catalog looks fully populated
before real photos exist. Swapping in real photos later is just setting
image_url normally — every image-rendering component already reads this
column, so no frontend code changes needed.

Run: python -m scripts.seed_images
"""
import asyncio

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.database import engine
from app.models.pet import Pet
from app.models.product import Product


async def seed_images():
    async with AsyncSession(engine) as session:
        products = (await session.exec(select(Product))).all()
        for product in products:
            product.image_url = f"https://picsum.photos/seed/product-{product.id}/600/450"
            session.add(product)

        pets = (await session.exec(select(Pet))).all()
        for pet in pets:
            pet.image_url = f"https://picsum.photos/seed/pet-{pet.id}/600/450"
            session.add(pet)

        await session.commit()
    print(f"Backfilled image_url for {len(products)} products and {len(pets)} pets.")


if __name__ == "__main__":
    asyncio.run(seed_images())
