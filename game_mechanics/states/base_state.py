from abc import ABC


class BaseState(ABC):
    """
    A state saves the different changeable elements of a Dominion game.
    """
    pass


class BasePlayerState(BaseState, ABC):
    """
    A state that saves the different changeable elements of a Dominion game related to a single player.
    """
    pass


class BasePublicState(BaseState, ABC):
    """
    A state that saves the different changeable elements of a Dominion game related to a single player.
    """
    pass
