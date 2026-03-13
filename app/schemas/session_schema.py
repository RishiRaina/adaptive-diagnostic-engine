from pydantic import BaseModel
from typing import List

class Session(BaseModel):
    user_id: str
    ability: float
    answered_questions: List[str]
    topics_wrong: List[str]