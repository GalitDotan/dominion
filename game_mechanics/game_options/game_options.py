from abc import ABC

from options import ServerOptions


class GameOptions(ServerOptions, ABC):
    """
    Represents a decision a curr_player has to make.
    """
    pass


