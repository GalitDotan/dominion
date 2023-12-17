from typing import Any

from game_mechanics.effects.effect import Effect
from game_mechanics.effects.player_decision import PlayerDecision


class Discard(Effect):
    def activate(self, game, player=None) -> Any:
        to_discard = game.apply_effect(PlayerDecision(), player)
        cards = player.hand.remove()
