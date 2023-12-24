from typing import Any

from game_mechanics.effects.effect import Effect


class PlayerDecisionEffect(Effect):
    """
    Receiving a decision from the player_name.
    """

    async def apply(self, game, player=None) -> Any:
        pass
