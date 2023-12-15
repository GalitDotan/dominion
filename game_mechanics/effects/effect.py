from abc import abstractmethod, ABC


class Effect(ABC):
    """
    An element that changes the state of the game/turn when applied.
    """

    @abstractmethod
    def activate(self, game):
        """
        Activate this effect according to a player's decision.

        Params:
            game: The current state of the game.
        """
        pass
