import sys
from pathlib import Path
from sqlalchemy.future import select

# Resolve backend root path
backend_path = Path(__file__).resolve().parent.parent.parent.parent
if str(backend_path) not in sys.path:
    sys.path.insert(0, str(backend_path))

from app.store.db import get_db
from app.store.models import Course, Flashcard

async def fetch_course_by_id(course_id: int) -> dict:
    """Retrieves course details and associated metadata from the database."""
    try:
        async for db in get_db():
            result = await db.execute(select(Course).where(Course.id == course_id))
            course = result.scalars().first()
            if not course:
                return {"status": "not_found", "message": f"Course ID {course_id} does not exist in database."}
            return {
                "id": course.id,
                "title": course.title,
                "description": course.description
            }
    except Exception as e:
        return {"status": "error", "details": str(e)}

async def fetch_cards_for_topic(topic_id: int) -> list:
    """Retrieves flashcard items for a specific study topic."""
    try:
        async for db in get_db():
            result = await db.execute(select(Flashcard).where(Flashcard.topic_id == topic_id))
            cards = result.scalars().all()
            return [{"id": card.id, "front": card.front, "back": card.back} for card in cards]
    except Exception as e:
        return [{"status": "error", "details": str(e)}]

