from typing import Optional

from pydantic import BaseModel

from consts import GameStatus
from game_mechanics.game_options.game_decisions import GameOptions


class ResponseModel(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    game_id: int
    game_status: GameStatus
    game_decision: Optional[GameOptions] = None
    message: Optional[str] = "Ok"
