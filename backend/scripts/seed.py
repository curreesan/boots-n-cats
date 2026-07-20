"""
Populates the DB with sample products, pets, and one staff user.
Run once after your tables exist: python -m scripts.seed

This is intentionally a script, not an API endpoint — there's no
"sign up as staff" flow by design (we cut the CMS user-management
idea), so the first staff account has to be created directly here,
same as any other seed data.
"""
import asyncio

from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.database import engine
from app.core.security import hash_password
from app.models.pet import Pet
from app.models.product import Product
from app.models.user import User

PRODUCTS = [
    Product(name="Squeaky Bone Toy", species="dog", category="toy", price=299, stock_quantity=50),
    Product(name="Cozy Cat Mat", species="cat", category="mat", price=799, stock_quantity=30),
    Product(name="Orthopedic Dog Bed", species="dog", category="bed", price=2499, stock_quantity=15),
    Product(name="Feather Wand Toy", species="cat", category="toy", price=349, stock_quantity=40),
    Product(name="Premium Kibble 5kg", species="dog", category="food", price=1299, stock_quantity=60),
]

PETS = [
    Pet(name="Bruno", species="dog", breed="Labrador", description="Playful, 2 years old, great with kids."),
    Pet(name="Whiskers", species="cat", breed="Persian", description="Calm, 4 years old, loves sunny windowsills."),
    Pet(name="Max", species="dog", breed="Beagle", description="Energetic, 1 year old, needs an active home."),
]


async def seed():
    """
    Inserts all sample products, pets, and one staff account in a single
    session. Since none of this data references each other (no foreign
    keys pointing between products/pets/the staff user), order doesn't
    matter and it's safe to add_all() everything before one commit.
    """
    async with AsyncSession(engine) as session:
        session.add_all(PRODUCTS)
        session.add_all(PETS)
        session.add(User(
            email="staff@bootsandcats.test",
            name="Store Staff",
            password_hash=hash_password("changeme123"),
            role="staff",
        ))
        await session.commit()
    print("Seeded products, pets, and one staff user (staff@bootsandcats.test / changeme123).")


if __name__ == "__main__":
    asyncio.run(seed())