from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, products, pets, orders, consultations, admin, knowledge
from fastapi.responses import HTMLResponse
from pathlib import Path

app = FastAPI(title="Boots and Cats API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite's default dev server address
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
app.include_router(consultations.router)
app.include_router(admin.router)
app.include_router(knowledge.router)

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