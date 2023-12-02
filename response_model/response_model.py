from typing import Optional

from pydantic import BaseModel

from game_status import GameStatus
from game_mechanics.decisions.game_decisions import GameDecision


class ResponseModel(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    game_id: int
    game_status: GameStatus
    game_decision: Optional[GameDecision] = None
    message: Optional[str] = "Ok"
