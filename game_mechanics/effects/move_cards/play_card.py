from typing import Any

from game_mechanics.effects.effect import Effect

"""
    if card not in self.state.hand:
        raise ValueError(f"{card} is not in {self.state.hand}")

    self.state.hand.remove(card)
    self.state.play_area.play(card)

    if isinstance(card, Treasure):
        turn_state.coins += card.coins
    if isinstance(card, Action):
        for cmd in card.actions:
            pass
    if isinstance(card, Attack):
        for cmd in card.attacks:
            pass
    if isinstance(card, Night):
        pass
"""


class PlayCard(Effect):
    def apply(self, game, player=None, card=None, *args, **kwargs) -> Any:
        # player.state.play_area.play(card)
        pass
