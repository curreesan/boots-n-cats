ADD_TO_CART_PROMPT = """
add_to_cart: to add a product to the cart, do these steps IN ORDER,
in the same turn, without stopping to ask permission in between:
1. Call search_products to get the product's real id (do this even if
   you already searched earlier — get a fresh id from this turn).
2. Call add_to_cart with that exact id and the requested quantity
   (default 1). This is a required step, not optional — a sentence
   like "I've added it" with no tool call is a failure.
3. Read add_to_cart's actual return value. Only if it says success,
   tell the user what was added (by name, never by id) and the new
   quantity. If it returned an error, tell the user that error — do
   not say it succeeded anyway.
""".strip()
