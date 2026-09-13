from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel
from app.store.db import get_db
from app.store.models import Topic
from app.graph.orchestrator import study_graph

router = APIRouter(prefix="/sessions", tags=["Sessions"])

class StartSessionRequest(BaseModel):
    topic_id: int

@router.post("/start")
async def start_session(req: StartSessionRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Topic).where(Topic.id == req.topic_id))
    topic = result.scalar_one_or_none()
    
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    initial_state = {
        "topic_id": topic.id,
        "topic_title": topic.title,
        "retrieved_context": "",
        "teacher_explanation": "",
        "quiz_questions": [],
        "quiz_score": None,
        "life_balance_output": {}
    }

    # Execute LangGraph Multi-Agent Cycle
    final_state = await study_graph.ainvoke(initial_state)

    return {
        "topic_id": topic.id,
        "topic_title": topic.title,
        "explanation": final_state.get("teacher_explanation"),
        "quiz": final_state.get("quiz_questions"),
        "life_balance": final_state.get("life_balance_output")
    }
