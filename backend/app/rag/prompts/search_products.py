SEARCH_PRODUCTS_PROMPT = """
search_products: call this for ANY catalog, pricing, or stock question,
and always immediately before add_to_cart to get the product's real id
— even if you searched earlier in this conversation, search again right
before adding, since the id must come from this turn's result.

If species/category filters return nothing, call it again with no
filters before telling the user the product doesn't exist — it may
exist under a different category than you guessed.
""".strip()
