from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.product import Product
from app.models.pet import Pet
from app.rag.retrieval import search_knowledge

PRODUCT_CATEGORIES = ["food", "furniture", "toy", "accessory", "others"]


def _normalize(value: str) -> str:
    """
    Lowercases and strips a trailing plural 's' (but not 'ss') — the model
    frequently passes "toys" for the DB's "toy", "dogs" for "dog", etc.
    An exact-match SQL filter would silently return zero rows on this kind
    of mismatch, which then reads to the model (and user) as "we don't
    stock that," even though matching rows exist. Normalizing both sides
    before comparing in Python avoids that false negative.
    """
    value = value.strip().lower()
    if value.endswith("s") and not value.endswith("ss"):
        value = value[:-1]
    return value


async def tool_search_knowledge(query: str) -> str:
    """Searches the knowledge base for policy/care information."""
    results = await search_knowledge(query)
    if not results:
        return "No relevant information found in the knowledge base."
    return "\n\n".join(f"[{r['source_filename']}] {r['text']}" for r in results)


async def tool_search_products(species: str | None, category: str | None, session: AsyncSession) -> str:
    """
    Searches the product catalog, optionally filtered. Includes each
    product's id in the output — required so add_to_cart has a real id
    to act on, the same reasoning as search_pets below.

    Filters in Python (not SQL) with normalized string comparison, so a
    plural/casing mismatch from the model (e.g. "toys" vs. the DB's "toy")
    doesn't silently return zero rows.
    """
    result = await session.exec(select(Product).where(Product.is_active))
    products = result.all()

    if species:
        target = _normalize(species)
        products = [p for p in products if _normalize(p.species) == target]
    if category:
        target = _normalize(category)
        products = [p for p in products if _normalize(p.category) == target]

    if not products:
        return (
            "No matching products found. Double-check the species/category "
            f"spelling — valid categories are: {', '.join(PRODUCT_CATEGORIES)}. "
            "If you didn't filter by category, try calling again with no "
            "filters to see the full catalog before telling the user it's unavailable."
        )
    return "\n".join(
        f"id={p.id} | {p.name} — ₹{p.price} ({p.stock_quantity} in stock)" for p in products
    )


async def tool_search_pets(species: str | None, session: AsyncSession) -> str:
    """
    Searches available pets, optionally filtered by species. Same
    Python-side normalized filtering as tool_search_products, for the
    same reason (avoid false "not found" on a plural/casing mismatch).
    """
    result = await session.exec(select(Pet).where(Pet.is_active))
    pets = result.all()

    if species:
        target = _normalize(species)
        pets = [p for p in pets if _normalize(p.species) == target]

    if not pets:
        return "No matching pets found. If you filtered by species, try again with no filter before telling the user none are available."
    return "\n".join(f"id={p.id} | {p.name} — {p.breed}, {p.species}: {p.description}" for p in pets)


async def tool_add_to_cart(product_id: str, quantity: int, user_id: str, session: AsyncSession) -> str:
    """
    Adds a product to the logged-in user's cart, incrementing its
    quantity if it's already there — same upsert behavior as POST /cart.
    """
    import uuid

    from app.models.cart import CartItem

    if quantity < 1:
        return "Error: quantity must be at least 1."

    try:
        product_uuid = uuid.UUID(product_id)
    except ValueError:
        return "Error: product_id must be a valid product id from search_products. Call search_products first to get it."

    product = await session.get(Product, product_uuid)
    if not product or not product.is_active:
        return "Error: no product found with that id. Call search_products first."

    user_uuid = uuid.UUID(user_id)
    result = await session.exec(
        select(CartItem).where(CartItem.user_id == user_uuid, CartItem.product_id == product_uuid)
    )
    existing = result.first()
    new_quantity = (existing.quantity if existing else 0) + quantity

    if new_quantity > product.stock_quantity:
        return f"Error: only {product.stock_quantity} of {product.name} in stock — can't add {quantity} more."

    product_name = product.name  # grab before commit expires the object's attributes

    if existing:
        existing.quantity = new_quantity
        session.add(existing)
    else:
        session.add(CartItem(user_id=user_uuid, product_id=product_uuid, quantity=new_quantity))

    await session.commit()
    return f"Added {quantity} x {product_name} to cart (now {new_quantity} total in cart)."


async def tool_request_checkout(user_id: str, session: AsyncSession) -> str:
    """
    Model-facing tool: validates the cart isn't empty, then signals the
    chat layer to show a real "Confirm order" button in the UI instead
    of trusting a text "YES" reply — same reasoning as
    tool_request_consultation: an irreversible action (this one decrements
    real stock and creates a permanent order) shouldn't be gated by the
    model's own judgment of whether the user really confirmed. run_agent
    special-cases the "SHOW_CHECKOUT:" marker to end the turn immediately.
    """
    import uuid

    from app.models.cart import CartItem

    user_uuid = uuid.UUID(user_id)
    result = await session.exec(select(CartItem).where(CartItem.user_id == user_uuid))
    cart_items = result.all()

    if not cart_items:
        return "The cart is empty — there's nothing to check out."

    item_count = sum(line.quantity for line in cart_items)
    return f"SHOW_CHECKOUT:{item_count}"


async def _find_pending_consultation(pet_uuid, user_uuid, session: AsyncSession):
    from app.models.consultation import AdoptionConsultation

    result = await session.exec(
        select(AdoptionConsultation).where(
            AdoptionConsultation.user_id == user_uuid,
            AdoptionConsultation.pet_id == pet_uuid,
            AdoptionConsultation.status == "requested",
        )
    )
    return result.first()


async def tool_request_consultation(pet_id: str, user_id: str, session: AsyncSession) -> str:
    """
    Model-facing tool: validates the pet exists and there's no duplicate
    pending request, then signals the chat layer to show a real date
    picker in the UI instead of collecting a date via free-text chat.

    Deliberately does NOT take a date/time argument and does NOT create
    the consultation itself — every attempt to get the model to reliably
    ask-for/validate a date in free text failed (it either skipped the
    ask entirely or fabricated a plausible-looking one no text heuristic
    could distinguish from a real answer). Moving date collection to an
    actual UI control removes the model from that trust boundary
    entirely: it can only ever trigger the picker, never supply the date.
    run_agent special-cases this tool's result (the "SHOW_PICKER:" prefix)
    to end the turn immediately instead of looping back to the model.
    """
    from app.models.pet import Pet
    import uuid

    try:
        pet_uuid = uuid.UUID(pet_id)
    except ValueError:
        return "Error: pet_id must be a valid pet id from search_pets. Call search_pets first to get it."

    pet = await session.get(Pet, pet_uuid)
    if not pet:
        return "Error: no pet found with that id. Call search_pets first."

    user_uuid = uuid.UUID(user_id)
    if await _find_pending_consultation(pet_uuid, user_uuid, session):
        return f"A consultation request for {pet.name} is already pending — no need to submit another."

    return f"SHOW_PICKER:{pet_id}:{pet.name}"


async def tool_create_consultation(pet_id: str, preferred_date: str, user_id: str, session: AsyncSession) -> str:
    """
    Creates a real adoption consultation request. Called directly by the
    websocket layer once the user submits the date picker triggered by
    tool_request_consultation — NOT part of the model's toolset, so
    preferred_date is always a real value from an actual <input
    type="date">, never model-generated text. Contact is read from the
    user's account email, same reasoning (never trust the model with it).
    """
    from app.models.consultation import AdoptionConsultation
    from app.models.pet import Pet
    from app.models.user import User
    import uuid

    try:
        pet_uuid = uuid.UUID(pet_id)
    except ValueError:
        return "Error: invalid pet id."

    pet = await session.get(Pet, pet_uuid)
    if not pet:
        return "Error: no pet found with that id."

    user_uuid = uuid.UUID(user_id)
    if await _find_pending_consultation(pet_uuid, user_uuid, session):
        return f"A consultation request for {pet.name} is already pending — no need to submit another."

    user = await session.get(User, user_uuid)
    contact = user.email

    pet_name = pet.name  # grab this BEFORE commit expires the object

    consultation = AdoptionConsultation(
        user_id=user_uuid,
        pet_id=pet_uuid,
        contact=contact,
        preferred_time=preferred_date,
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
            "description": "Search the product catalog by species and/or category. Omit both to list the entire catalog.",
            "parameters": {
                "type": "object",
                "properties": {
                    "species": {"type": "string", "enum": ["dog", "cat"], "description": "optional"},
                    "category": {"type": "string", "enum": PRODUCT_CATEGORIES, "description": "optional — omit rather than guess if unsure"},
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_pets",
            "description": "Search available pets for adoption by species. Omit species to list all available pets.",
            "parameters": {
                "type": "object",
                "properties": {
                    "species": {"type": "string", "enum": ["dog", "cat"], "description": "optional"}
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "add_to_cart",
            "description": "Actually adds a product to the logged-in user's cart — call this to perform the add, not just to describe it. Requires a real product_id from search_products.",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_id": {"type": "string", "description": "The product's id, from search_products"},
                    "quantity": {"type": "integer", "description": "How many to add — defaults to 1 if not specified"},
                },
                "required": ["product_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "request_checkout",
            "description": (
                "Call this when the user wants to place their order / check out. This "
                "shows the user a real 'Confirm order' button in the chat UI — do NOT "
                "ask the user to confirm in text, do NOT say the order was placed "
                "yourself. Just call this with no arguments and let the UI handle it."
            ),
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "request_consultation",
            "description": (
                "Call this once the user has expressed interest in adopting a specific pet. "
                "This shows the user a real date picker in the chat UI to choose their preferred "
                "callback date — do NOT ask the user for a date/time yourself, do NOT ask for "
                "contact info, and do NOT try to collect or confirm any date in text. Just call "
                "this with the pet's id and let the UI handle the rest."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "pet_id": {"type": "string", "description": "The pet's id, from search_pets"},
                },
                "required": ["pet_id"],
            },
        },
    },
]