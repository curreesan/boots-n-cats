# Boots and Cats

A full-stack pet store with an agentic RAG chatbot — browse products and pets, manage a
persistent cart, check out, book adoption consultations, and get help from an AI assistant
that can actually search the catalog, add items to your cart, and place orders on your behalf.

**Live demo:** _TBD — link coming after deployment_

## Features

- Product & pet catalog with pagination, species/category filters, and admin inline editing
- Server-side persistent cart, checkout with atomic stock decrement, order history
- Adoption consultation booking with a real date picker (no free-text date guessing)
- Agentic chatbot (WebSocket-based) that can search the knowledge base, search products/pets,
  add items to your cart, and walk you through checkout — with UI-driven confirmation for
  anything consequential (placing an order, booking a consultation) so the model is never
  trusted to fabricate a date, price, or confirmation on its own
- Cookie-based JWT auth (access + refresh tokens), role-gated admin area

## Stack

- **Backend:** FastAPI + SQLModel + Alembic, Supabase (Postgres) via asyncpg
- **Frontend:** React + TypeScript + Vite + Tailwind v4 + shadcn/ui
- **AI:** Cloudflare Workers AI for chat (tool-calling) and embeddings, Pinecone for vector
  storage, Supabase Storage for images

## Running locally

**Backend**
```
cd backend
python -m venv venv && venv\Scripts\activate   # or source venv/bin/activate on macOS/Linux
pip install -r requirements.txt
# copy .env.example to .env and fill in your own keys (DB, Pinecone, Cloudflare, Supabase)
uvicorn app.main:app --reload
```

**Frontend**
```
cd frontend
npm install
npm run dev
```

The frontend expects the backend at `VITE_API_BASE_URL` (defaults to `http://localhost:8000`
if unset) and the backend expects the frontend's origin at `FRONTEND_URL` for CORS.
