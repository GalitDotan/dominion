from typing import Optional

from pydantic import BaseModel

from consts import GameStatus


class ResponseModel(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    game_id: int
    game_status: GameStatus
    message: Optional[str] = "Ok"
