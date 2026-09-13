def query_vector_notes(query_text: str, n_results: int = 3) -> dict:
    """Queries ChromaDB vector store for relevant lecture context and textbook notes."""
    try:
        from app.store.chroma import query_chroma
        results = query_chroma(query_text=query_text, n_results=n_results)
        documents = results.get("documents", [[]])[0] if results else []
        return {"retrieved_context": documents}
    except Exception as e:
        return {"error": str(e), "retrieved_context": []}

