from typing import Any

from game_mechanics.effects.effect import Effect
from game_mechanics.effects.reactions.on_effect_reaction import Reaction


class AddReaction(Effect):
    def __init__(self, reaction: Reaction):
        super().__init__()
        self.reaction = reaction

    def apply(self, game, player=None, *args, **kwargs) -> Any:
        game.add_waiting_reaction(self.reaction, player)

    def un_activate(self, game, player=None, *args, **kwargs) -> Any:
        pass
