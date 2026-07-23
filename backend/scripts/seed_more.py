"""
Adds a larger batch of sample products and pets on top of what seed.py
already inserted — enough to push both past the default page size (20),
so pagination actually has a second page to exercise.

Separate from seed.py (not just re-running it with more data) because
seed.py also inserts the staff user, and running it twice would collide
with the unique constraint on email. This script only touches products
and pets. Run once: python -m scripts.seed_more
"""
import asyncio

from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.database import engine
from app.models.pet import Pet
from app.models.product import Product

MORE_PRODUCTS = [
    Product(name="Rope Tug Toy", species="dog", category="toy", price=249, stock_quantity=45),
    Product(name="Catnip Mouse", species="cat", category="toy", price=149, stock_quantity=60),
    Product(name="Waterproof Dog Coat", species="dog", category="apparel", price=899, stock_quantity=25),
    Product(name="Scratching Post", species="cat", category="furniture", price=1599, stock_quantity=18),
    Product(name="Grain-Free Cat Food 3kg", species="cat", category="food", price=999, stock_quantity=40),
    Product(name="Dog Chew Bone", species="dog", category="toy", price=199, stock_quantity=70),
    Product(name="Cat Carrier Bag", species="cat", category="travel", price=1299, stock_quantity=20),
    Product(name="Dog Leash 2m", species="dog", category="accessory", price=399, stock_quantity=55),
    Product(name="Cat Litter Box", species="cat", category="hygiene", price=1099, stock_quantity=30),
    Product(name="Dog Raincoat", species="dog", category="apparel", price=799, stock_quantity=22),
    Product(name="Interactive Puzzle Feeder", species="dog", category="toy", price=649, stock_quantity=35),
    Product(name="Cat Tunnel Toy", species="cat", category="toy", price=449, stock_quantity=28),
    Product(name="Puppy Training Pads (50pk)", species="dog", category="hygiene", price=549, stock_quantity=60),
    Product(name="Cat Grooming Brush", species="cat", category="grooming", price=299, stock_quantity=50),
    Product(name="Dog Grooming Brush", species="dog", category="grooming", price=299, stock_quantity=50),
    Product(name="Elevated Food Bowl", species="dog", category="feeding", price=699, stock_quantity=33),
    Product(name="Cat Feeding Bowl Set", species="cat", category="feeding", price=499, stock_quantity=40),
    Product(name="Dog Kennel (Medium)", species="dog", category="bed", price=3499, stock_quantity=10),
    Product(name="Cat Bed Igloo", species="cat", category="bed", price=1799, stock_quantity=15),
    Product(name="Squeaky Duck Toy", species="dog", category="toy", price=179, stock_quantity=65),
]

MORE_PETS = [
    Pet(name="Luna", species="cat", breed="Siamese", description="Playful, 1 year old, loves chasing laser pointers."),
    Pet(name="Rocky", species="dog", breed="German Shepherd", description="Loyal, 3 years old, great guard dog."),
    Pet(name="Milo", species="cat", breed="Tabby", description="Curious, 6 months old, very affectionate."),
    Pet(name="Daisy", species="dog", breed="Golden Retriever", description="Friendly, 2 years old, good with other pets."),
    Pet(name="Shadow", species="cat", breed="Bombay", description="Independent, 5 years old, enjoys quiet spaces."),
    Pet(name="Cooper", species="dog", breed="Poodle", description="Smart, 1 year old, hypoallergenic coat."),
    Pet(name="Coco", species="cat", breed="Ragdoll", description="Gentle, 2 years old, loves being carried."),
    Pet(name="Buddy", species="dog", breed="Bulldog", description="Laid-back, 4 years old, short daily walks needed."),
    Pet(name="Simba", species="cat", breed="Maine Coon", description="Large and gentle, 3 years old, great with kids."),
    Pet(name="Zeus", species="dog", breed="Rottweiler", description="Protective, 2 years old, needs an experienced owner."),
    Pet(name="Nala", species="cat", breed="Persian", description="Calm, 4 years old, needs regular grooming."),
    Pet(name="Charlie", species="dog", breed="Dachshund", description="Curious, 1 year old, loves digging."),
    Pet(name="Oliver", species="cat", breed="British Shorthair", description="Chill, 2 years old, low maintenance."),
    Pet(name="Bella", species="dog", breed="Border Collie", description="Highly active, 2 years old, needs mental stimulation."),
    Pet(name="Mimi", species="cat", breed="Sphynx", description="Affectionate, 1 year old, needs indoor warmth."),
    Pet(name="Duke", species="dog", breed="Boxer", description="Energetic, 3 years old, great with active families."),
    Pet(name="Pepper", species="cat", breed="Scottish Fold", description="Sweet, 2 years old, folded ears, very social."),
    Pet(name="Rex", species="dog", breed="Doberman", description="Alert, 4 years old, needs firm training."),
    Pet(name="Toby", species="dog", breed="Shih Tzu", description="Small and friendly, 2 years old, good for apartments."),
    Pet(name="Cleo", species="cat", breed="Abyssinian", description="Energetic, 1 year old, loves climbing."),
]


async def seed_more():
    async with AsyncSession(engine) as session:
        session.add_all(MORE_PRODUCTS)
        session.add_all(MORE_PETS)
        await session.commit()
    print(f"Added {len(MORE_PRODUCTS)} more products and {len(MORE_PETS)} more pets.")


if __name__ == "__main__":
    asyncio.run(seed_more())
