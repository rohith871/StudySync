import json
from langchain_openai import ChatOpenAI
from app.config import settings
from app.graph.state import StudySyncState

async def quiz_node(state: StudySyncState) -> dict:
    explanation = state["teacher_explanation"]
    topic_title = state["topic_title"]

    # Initialize Grok via OpenAI compatibility layer
    llm = ChatOpenAI(
        model="grok-4.1-fast",
        api_key=settings.GROK_API_KEY,
        base_url="https://api.x.ai/v1"
    )

    # Enforce Strict Context Bounding to avoid out-of-domain questions
    prompt = f"""
    You are an exam generator. Create 3 multiple choice questions for the topic '{topic_title}'.

    CRITICAL RULE: Questions must be answerable using ONLY facts explicitly mentioned in the Lesson Text below.
    Do NOT use outside knowledge.

    Lesson Text:
    {explanation}

    Return ONLY a raw JSON array matching this exact schema, without markdown tags:
    [
      {{
        "id": 1,
        "question": "Question text here",
        "options": ["Option A", "Option B", "Option C", "Option D"],
        "answer": "Option A"
      }}
    ]
    """
    
    response = await llm.ainvoke(prompt)
    content = str(response.content).strip()
    
    # Strip markdown block formatting if present
    if content.startswith("```json"):
        content = content.replace("```json", "").replace("```", "").strip()
    elif content.startswith("```"):
        content = content.replace("```", "").strip()

    try:
        questions = json.loads(content)
    except Exception:
        questions = []

    return {"quiz_questions": questions}
