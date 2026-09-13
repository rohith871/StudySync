import chromadb
from app.config import settings

# Initialize ChromaDB persistent client
chroma_client = chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIR)
collection = chroma_client.get_or_create_collection(name="studysync_notes")

def add_documents_to_chroma(topic_id: str, texts: list[str], metadata: list[dict]):
    """Store vectorized note chunks."""
    ids = [f"{topic_id}_chunk_{i}" for i in range(len(texts))]
    collection.add(documents=texts, metadatas=metadata, ids=ids)

def query_chroma(query_text: str, n_results: int = 3):
    """Retrieve top-K matching notes for RAG."""
    results = collection.query(query_texts=[query_text], n_results=n_results)
    return results
