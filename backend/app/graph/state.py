from typing import TypedDict, List, Dict, Any, Optional

class StudySyncState(TypedDict):
    topic_id: int
    topic_title: str
    retrieved_context: str
    teacher_explanation: str
    quiz_questions: List[Dict[str, Any]]
    quiz_score: Optional[float]
    life_balance_output: Dict[str, Any]
    