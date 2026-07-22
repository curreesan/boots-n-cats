from app.rag.retrieval import search_knowledge

results = search_knowledge("what is your adoption policy")
for r in results:
    print(r["score"], r["source_filename"], r["text"][:80])