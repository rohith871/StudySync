from app.mcp_server.server import compute_life_balance
from app.graph.state import StudySyncState

async def life_balance_node(state: StudySyncState) -> dict:
    # Run FastMCP life balance tool to update budget
    output = compute_life_balance(upcoming_assignments=1, recent_study_hours=1.5)
    return {"life_balance_output": output}
