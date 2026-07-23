SEARCH_PETS_PROMPT = """
search_pets: call this for any question about pets available for
adoption, and always immediately before create_consultation to get the
pet's real id from this turn's result. If a species filter returns
nothing, call it again with no filter before telling the user no pets
of that kind are available.
""".strip()
