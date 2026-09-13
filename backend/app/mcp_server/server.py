import sys
from pathlib import Path

# Resolve path to 'backend/' directory (3 levels up from server.py)
backend_path = Path(__file__).resolve().parent.parent.parent
if str(backend_path) not in sys.path:
    sys.path.insert(0, str(backend_path))

from fastmcp import FastMCP
from app.mcp_server.tools.sm2_tools import calculate_sm2_review
from app.mcp_server.tools.rag_tools import query_vector_notes
from app.mcp_server.tools.db_tools import fetch_course_by_id, fetch_cards_for_topic

mcp = FastMCP(name="StudySync_Tools")

@mcp.tool()
def compute_life_balance(upcoming_assignments: int, recent_study_hours: float) -> dict:
    """Calculates daily leisure budget based on workload."""
    base_budget = 3.0
    assignment_penalty = min(upcoming_assignments * 0.5, 2.0)
    study_reward = min(recent_study_hours * 0.2, 1.5)
    final_budget = max(base_budget - assignment_penalty + study_reward, 1.0)

    return {
        "daily_leisure_hours": round(final_budget, 1),
        "reasoning": f"Base 3.0h. Penalty of -{assignment_penalty}h. Reward of +{study_reward}h."
    }

@mcp.tool()
def calculate_sm2(quality: int, previous_ef: float, repetitions: int, previous_interval: int) -> dict:
    """SuperMemo-2 (SM-2) Spaced Repetition Tool."""
    return calculate_sm2_review(quality, previous_ef, repetitions, previous_interval)

@mcp.tool()
def query_course_notes(query_text: str, n_results: int = 3) -> dict:
    """Vector search tool for course notes in ChromaDB."""
    return query_vector_notes(query_text, n_results)

@mcp.tool()
async def get_course_data(course_id: int) -> dict:
    """Database lookup tool for course metadata."""
    return await fetch_course_by_id(course_id)

@mcp.tool()
async def get_topic_flashcards(topic_id: int) -> list:
    """Database lookup tool for topic flashcards."""
    return await fetch_cards_for_topic(topic_id)

if __name__ == "__main__":
    mcp.run()
    