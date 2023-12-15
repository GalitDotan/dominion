from abc import abstractmethod, ABC
from typing import Optional


class Effect(ABC):
    """
    An element that changes the state of the game/turn when applied.
    """

    def __init__(self, name: Optional[str] = None):
        self.name = name if name else self.__class__.__name__

    def __repr__(self):
        return self.name

    @abstractmethod
    def activate(self, game):
        """
        Activate this effect according to a player's decision.

        Params:
            game: The current state of the game.
        """
        pass
