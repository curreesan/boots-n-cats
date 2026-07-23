import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, products, pets, orders, cart, consultations, admin, knowledge, chat, websocket_chat
from fastapi.responses import HTMLResponse, JSONResponse
from pathlib import Path

from app.core.config import settings
from app.core.exceptions import NotFoundError
from app.core.logging import configure_logging

configure_logging()
logger = logging.getLogger(__name__)

app = FastAPI(title="Boots and Cats API")


@app.exception_handler(NotFoundError)
async def not_found_handler(request: Request, exc: NotFoundError):
    """Turns any raised NotFoundError into a 404 with the same {"detail": ...} shape every other error uses."""
    return JSONResponse(status_code=404, content={"detail": exc.message})


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    """
    Catches anything that isn't an HTTPException, RequestValidationError,
    or NotFoundError — i.e. a genuine bug, not an expected error case.
    FastAPI/Starlette match handlers by the exception's exact type first,
    so HTTPException and NotFoundError are still handled by their own
    handlers above and never reach this one. Logs the full traceback
    server-side (so it's actually debuggable) but never leaks internal
    details to the client — just a generic 500 in the same shape.
    """
    logger.exception("Unhandled exception on %s %s", request.method, request.url.path)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True, # lets the browser send/receive our auth cookies cross-origin
    allow_methods=["*"],
    allow_headers=["*"],
)

# Each router owns one resource's endpoints — matches the domain breakdown
# we designed earlier. This file's only job is wiring things together;
# if you're looking for actual logic, it's never here, it's in routers/.
app.include_router(auth.router)
app.include_router(products.router)
app.include_router(pets.router)
app.include_router(orders.router)
app.include_router(cart.router)
app.include_router(consultations.router)
app.include_router(admin.router)
app.include_router(knowledge.router)
app.include_router(chat.router)
app.include_router(websocket_chat.router)

@app.get("/", response_class=HTMLResponse)
async def root():
    """
    Serves the static route-index page at the bare root URL — this is what
    used to 404 back when we first started the server. Not a real API
    endpoint, just a human-readable map of what's available.
    """
    html_path = Path(__file__).parent.parent / "static" / "index.html"
    return html_path.read_text(encoding="utf-8")

@app.get("/health")
async def health():
    """
    A trivial endpoint with no dependencies at all — not part of the
    store's actual functionality. Useful as a quick sanity check that the
    server is up and reachable, before worrying about auth, the database,
    or anything else. Also the kind of endpoint hosting platforms often
    ping automatically to check if your app is alive.
    """
    return {"status": "ok"}