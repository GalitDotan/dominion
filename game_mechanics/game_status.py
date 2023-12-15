from enum import Enum


class GameStatus(Enum):
    """
    The current status of a game.
    """
    INITIATED = 'INITIATED'
    IN_PROGRESS = 'IN_PROGRESS'
    FINISHED = 'FINISHED'
