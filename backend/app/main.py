from fastapi import FastAPI

from app.routers import auth, products, pets, cart, orders, consultations, admin

app = FastAPI(title="Boots and Cats API")

# Each router owns one resource's endpoints — matches the domain breakdown
# we designed earlier. This file's only job is wiring things together;
# if you're looking for actual logic, it's never here, it's in routers/.
app.include_router(auth.router)
app.include_router(products.router)
app.include_router(pets.router)
app.include_router(cart.router)
app.include_router(orders.router)
app.include_router(consultations.router)
app.include_router(admin.router)


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