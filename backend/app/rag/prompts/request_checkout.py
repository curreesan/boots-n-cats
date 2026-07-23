REQUEST_CHECKOUT_PROMPT = """
request_checkout: when the user wants to place their order or check
out, call request_checkout immediately — no arguments needed, no text
confirmation from you first. The chat UI shows a real "Confirm order"
button and handles the actual placing of the order itself.

Do NOT ask the user to confirm in text, do NOT say the order was
placed (the UI reports that once the user actually clicks Confirm).
If the tool says the cart is empty, tell the user that.
""".strip()
