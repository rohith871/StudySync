from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.store.db import get_db
from app.store.models import Flashcard
from app.mcp_server.server import calculate_sm2
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/flashcards", tags=["Flashcards"])

class FlashcardCreate(BaseModel):
    topic_id: int
    front: str
    back: str

class FlashcardReview(BaseModel):
    quality: int

@router.post("/")
async def create_flashcard(card: FlashcardCreate, db: AsyncSession = Depends(get_db)):
    new_card = Flashcard(topic_id=card.topic_id, front=card.front, back=card.back)
    db.add(new_card)
    await db.commit()
    await db.refresh(new_card)
    return new_card

@router.post("/{card_id}/review")
async def review_flashcard(card_id: int, review: FlashcardReview, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Flashcard).where(Flashcard.id == card_id))
    card = result.scalar_one_or_none()
    
    if not card:
        raise HTTPException(status_code=404, detail="Flashcard not found")

    # Pass current stats to FastMCP tool
    sm2_results = calculate_sm2(
        quality=review.quality,
        previous_ef=card.easiness_factor,
        repetitions=card.repetitions,
        previous_interval=card.interval
    )
    
    # Update Flashcard parameters
    card.easiness_factor = sm2_results["easiness_factor"]
    card.repetitions = sm2_results["repetitions"]
    card.interval = sm2_results["interval"]
    card.next_review = datetime.fromisoformat(sm2_results["next_review"])
    
    await db.commit()
    await db.refresh(card)
    return {"status": "Reviewed successfully", "next_review": card.next_review}
