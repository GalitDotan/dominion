from typing import Any

from game_mechanics.effects.effect import Effect
from game_mechanics.effects.player_decision import PlayerDecision


class Draw(Effect):
    def activate(self, game, player=None) -> Any:
        decision = game.apply_effect(PlayerDecision(), player)
        player.draw(decision.num)
