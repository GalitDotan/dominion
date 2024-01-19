from typing import Any

from game_mechanics.effects.effect import Effect
from game_mechanics.effects.player_decision import PlayerCheckboxChoice


class Discard(Effect):
    async def apply(self, game, player=None, **kwargs) -> Any:
        to_discard = await game.apply_effect(PlayerCheckboxChoice(player.hand.cards), player)
        cards = player.hand.remove(to_discard)
        return cards
