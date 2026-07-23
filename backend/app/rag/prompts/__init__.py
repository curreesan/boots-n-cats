"""
The system prompt is assembled from one file per concern — a shared base,
plus one block per tool — instead of a single monolithic string. Changing
how the model uses search_products, say, means editing search_products.py
only, without scrolling past every other tool's instructions to find it.
"""

from app.rag.prompts.base import BASE_PROMPT
from app.rag.prompts.search_knowledge import SEARCH_KNOWLEDGE_PROMPT
from app.rag.prompts.search_products import SEARCH_PRODUCTS_PROMPT
from app.rag.prompts.search_pets import SEARCH_PETS_PROMPT
from app.rag.prompts.add_to_cart import ADD_TO_CART_PROMPT
from app.rag.prompts.request_checkout import REQUEST_CHECKOUT_PROMPT
from app.rag.prompts.create_consultation import CREATE_CONSULTATION_PROMPT


def build_system_prompt() -> str:
    """Unites every prompt block, in order, into the single string actually sent to the model."""
    return "\n\n".join([
        BASE_PROMPT,
        SEARCH_KNOWLEDGE_PROMPT,
        SEARCH_PRODUCTS_PROMPT,
        SEARCH_PETS_PROMPT,
        ADD_TO_CART_PROMPT,
        REQUEST_CHECKOUT_PROMPT,
        CREATE_CONSULTATION_PROMPT,
    ])
