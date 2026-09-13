from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.store.db import get_db
from app.store.models import Course, Topic
from app.store.chroma import add_documents_to_chroma
from pydantic import BaseModel

router = APIRouter(prefix="/courses", tags=["Courses"])

class CourseCreate(BaseModel):
    title: str
    description: str

class TopicCreate(BaseModel):
    course_id: int
    title: str
    content: str

@router.post("/")
async def create_course(course: CourseCreate, db: AsyncSession = Depends(get_db)):
    new_course = Course(title=course.title, description=course.description)
    db.add(new_course)
    await db.commit()
    await db.refresh(new_course)
    return new_course

@router.post("/topics")
async def create_topic(topic: TopicCreate, db: AsyncSession = Depends(get_db)):
    new_topic = Topic(course_id=topic.course_id, title=topic.title, content=topic.content)
    db.add(new_topic)
    await db.commit()
    await db.refresh(new_topic)
    
    # Store note content in ChromaDB for AI RAG retrieval later
    add_documents_to_chroma(
        topic_id=str(new_topic.id),
        texts=[topic.content],
        metadata=[{"course_id": topic.course_id, "topic_title": topic.title}]
    )
    
    return {"status": "Topic embedded securely", "topic_id": new_topic.id}
