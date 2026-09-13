from langchain_google_genai import ChatGoogleGenerativeAI
from app.config import settings
from app.store.chroma import query_chroma
from app.graph.state import StudySyncState

async def teacher_node(state: StudySyncState) -> dict:
    topic_title = state["topic_title"]
    
    # 1. Fetch RAG context from ChromaDB
    rag_res = query_chroma(query_text=topic_title, n_results=3)
    docs = rag_res.get("documents", [[]])[0]
    context = "\n---\n".join(docs) if docs else "No specific notes ingested for this topic."

    # 2. Generate detailed explanation using Gemini
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=settings.GOOGLE_API_KEY
    )
    
    prompt = f"""
    You are an expert tutor in StudySync. Provide a clear, structured, and engaging study lesson for the topic '{topic_title}'.
    Use the following course notes as context.

    Context Notes:
    {context}
    """
    
    response = await llm.ainvoke(prompt)
    
    return {
        "retrieved_context": context,
        "teacher_explanation": response.content
    }
