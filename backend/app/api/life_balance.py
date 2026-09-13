from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.store.db import get_db
from app.store.models import LifeBalanceBudget
from app.mcp_server.server import compute_life_balance
from pydantic import BaseModel

router = APIRouter(prefix="/life-balance", tags=["Life Balance"])

class WorkloadMetrics(BaseModel):
    upcoming_assignments: int
    recent_study_hours: float

@router.post("/compute")
async def calculate_budget(metrics: WorkloadMetrics, db: AsyncSession = Depends(get_db)):
    # Run the FastMCP logic block
    budget_data = compute_life_balance(
        upcoming_assignments=metrics.upcoming_assignments,
        recent_study_hours=metrics.recent_study_hours
    )
    
    # Commit decision logging
    record = LifeBalanceBudget(
        daily_leisure_hours=budget_data["daily_leisure_hours"],
        reasoning=budget_data["reasoning"]
    )
    db.add(record)
    await db.commit()
    await db.refresh(record)
    
    return record
