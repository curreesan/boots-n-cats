class NotFoundError(Exception):
    """
    Raised anywhere a lookup by id comes up empty. Routes raise this
    instead of building HTTPException(status_code=404, ...) directly —
    the global handler registered in main.py is what actually turns it
    into a 404 response, so every "not found" across the whole API
    replies with the exact same {"detail": "..."} shape without each
    route repeating that translation itself.
    """

    def __init__(self, message: str):
        self.message = message
