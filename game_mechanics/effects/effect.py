from abc import abstractmethod, ABC
from typing import Optional, Any
from uuid import uuid4


class Effect(ABC):
    """
    An element that changes the state of the game/turn when applied.
    """

    def __init__(self, name: Optional[str] = None, is_disabled: bool = False):
        self.name = name if name else self.__class__.__name__
        self.id = str(uuid4())
        self.is_disabled: bool = is_disabled

    def __repr__(self):
        return self.name

    async def activate(self, game, player=None, *args, **kwargs) -> Any:
        """
        Activate this effect.

        Args:
            game: The current state of the game.
            player: The player.
        """
        if self.is_disabled:
            return
        return await self.apply(game, player, *args, **kwargs)

    @abstractmethod
    async def apply(self, game, player=None, *args, **kwargs) -> Any:
        """
        The actual logic that is applied on activation. 
        """
        pass

    def un_activate(self, game, player=None, *args, **kwargs) -> Any:
        """
        Un-activate this effect.

        Args:
            game: The current state of the game.
            player: The player.
        """
        return
