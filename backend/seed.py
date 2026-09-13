import asyncio
import sys
from pathlib import Path

# Ensure backend root is in sys.path
backend_path = Path(__file__).resolve().parent
if str(backend_path) not in sys.path:
    sys.path.insert(0, str(backend_path))

from app.store.db import init_db, AsyncSessionLocal
from app.store.models import Course, Flashcard

async def seed():
    # Ensure database tables exist
    await init_db()

    async with AsyncSessionLocal() as session:
        async with session.begin():
            # Add sample course
            sample_course = Course(
                title="Computer Science 101",
                description="Introduction to Algorithms and Data Structures"
            )
            session.add(sample_course)

            # Add sample flashcards for topic_id = 1
            card_1 = Flashcard(
                topic_id=1,
                front="What is the time complexity of Binary Search?",
                back="O(log n)"
            )
            card_2 = Flashcard(
                topic_id=1,
                front="What does FIFO stand for?",
                back="First In, First Out (Queue data structure)"
            )
            session.add_all([card_1, card_2])

        await session.commit()
    print("Database seeded successfully!")

if __name__ == "__main__":
    asyncio.run(seed())

