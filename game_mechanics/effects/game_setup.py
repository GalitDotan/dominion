from typing import Any

from game_mechanics.effects.effect import Effect
from game_mechanics.effects.move_cards.draw_num_cards import DrawNum


class GameSetup(Effect):
    def __init__(self):
        super().__init__()
        self.cards_to_draw = 5

    async def apply(self, game, player=None, **kwargs) -> Any:
        """
        Each player_name draws cards.
        """
        for player in game.players.values():
            await game.apply_effect(DrawNum(self.cards_to_draw), player)
