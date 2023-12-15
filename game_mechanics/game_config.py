from enum import Enum
from uuid import uuid4

from pydantic import BaseModel, Field


class GameStatus(Enum):
    """
    The current status of a game.
    """
    INITIATED = 'INITIATED'
    IN_PROGRESS = 'IN_PROGRESS'
    FINISHED = 'FINISHED'


class GameConfiguration(BaseModel):
    """
    The configuration of the game:
    Which cards does the game include,
    The players.
    """

    class Config:
        arbitrary_types_allowed = True

    game_id: str = Field(default_factory=lambda: str(uuid4()))
    player_names: list[str] = []
    status: GameStatus = GameStatus.INITIATED
    kingdom_piles: list[str] = []  # TODO
    standard_piles: list[str] = []  # TODO

    def __hash__(self):
        return hash(self.game_id)

    def __repr__(self):
        return f'{self.game_id}[{self.status}]:{self.player_names}'
