from langgraph.graph import StateGraph, END
from app.graph.state import StudySyncState
from app.graph.nodes.teacher import teacher_node
from app.graph.nodes.quiz import quiz_node
from app.graph.nodes.life_balance import life_balance_node

def build_graph():
    workflow = StateGraph(StudySyncState)
    
    # Add agent nodes
    workflow.add_node("teacher", teacher_node)
    workflow.add_node("quiz", quiz_node)
    workflow.add_node("life_balance", life_balance_node)

    # Wire graph flow: Gemini Teacher -> Grok Quiz -> FastMCP LifeBalance -> End
    workflow.set_entry_point("teacher")
    workflow.add_edge("teacher", "quiz")
    workflow.add_edge("quiz", "life_balance")
    workflow.add_edge("life_balance", END)

    return workflow.compile()

study_graph = build_graph()
