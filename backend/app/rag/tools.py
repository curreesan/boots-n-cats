from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.product import Product
from app.models.pet import Pet
from app.rag.retrieval import search_knowledge


async def tool_search_knowledge(query: str) -> str:
    """Searches the knowledge base for policy/care information."""
    results = search_knowledge(query)
    if not results:
        return "No relevant information found in the knowledge base."
    return "\n\n".join(f"[{r['source_filename']}] {r['text']}" for r in results)


async def tool_search_products(species: str | None, category: str | None, session: AsyncSession) -> str:
    """Searches the product catalog, optionally filtered."""
    query = select(Product)
    if species:
        query = query.where(Product.species == species)
    if category:
        query = query.where(Product.category == category)

    result = await session.exec(query)
    products = result.all()

    if not products:
        return "No matching products found."
    return "\n".join(f"{p.name} — ₹{p.price} ({p.stock_quantity} in stock)" for p in products)


async def tool_search_pets(species: str | None, session: AsyncSession) -> str:
    """Searches available pets, optionally filtered by species."""
    query = select(Pet)
    if species:
        query = query.where(Pet.species == species)

    result = await session.exec(query)
    pets = result.all()

    if not pets:
        return "No matching pets found."
    return "\n".join(f"id={p.id} | {p.name} — {p.breed}, {p.species}: {p.description}" for p in pets)

async def tool_create_consultation(pet_id: str, contact: str, preferred_time: str, user_id: str, session: AsyncSession) -> str:
    """Creates a real adoption consultation request tied to the logged-in user."""
    from app.models.consultation import AdoptionConsultation
    from app.models.pet import Pet
    import uuid

    try:
        pet_uuid = uuid.UUID(pet_id)
    except ValueError:
        return "Error: pet_id must be a valid pet id from search_pets. Call search_pets first to get it."

    pet = await session.get(Pet, pet_uuid)
    if not pet:
        return "Error: no pet found with that id. Call search_pets first."

    pet_name = pet.name  # grab this BEFORE commit expires the object

    consultation = AdoptionConsultation(
        user_id=user_id,
        pet_id=pet_uuid,
        contact=contact,
        preferred_time=preferred_time,
    )
    session.add(consultation)
    await session.commit()
    return f"Consultation request submitted for {pet_name}."

# Tool schemas — this is what actually gets sent to the LLM, describing
# what each tool does and what arguments it expects. The LLM reads these
# descriptions to decide when and how to call each one.
TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "search_knowledge",
            "description": "Search store policies, care guides, and FAQs for factual information.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The question to search for"}
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_products",
            "description": "Search the product catalog by species and/or category.",
            "parameters": {
                "type": "object",
                "properties": {
                    "species": {"type": "string", "description": "'dog' or 'cat', optional"},
                    "category": {"type": "string", "description": "e.g. 'toy', 'food', optional"},
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_pets",
            "description": "Search available pets for adoption by species.",
            "parameters": {
                "type": "object",
                "properties": {
                    "species": {"type": "string", "description": "'dog' or 'cat', optional"}
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "create_consultation",
            "description": "Submit an adoption consultation request for a specific pet. Only call this AFTER the user has explicitly confirmed they want to proceed.",
            "parameters": {
                "type": "object",
                "properties": {
                    "pet_id": {"type": "string", "description": "The pet's id, from search_pets"},
                    "contact": {"type": "string", "description": "Phone or email"},
                    "preferred_time": {"type": "string", "description": "Preferred callback time"},
                },
                "required": ["pet_id", "contact", "preferred_time"],
            },
        },
    },
]