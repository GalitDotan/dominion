from typing import Any, Callable

from game_mechanics.effects.effect import Effect
from game_mechanics.effects.gain_cards import GainCardsToHand
from game_mechanics.effects.player_decision import PlayerDecision
from game_mechanics.game_supplies.base_card import Card


class TrashFromHand(Effect):
    async def apply(self, game, player=None, *args, **kwargs) -> Any:
        treasure = await game.apply_effect(PlayerDecision(player.hand.cards), player)
        player.hand.remove(treasure)
        player.remove_card(treasure)
        game.trash.append(treasure)
        return treasure


class TrashThenGain(Effect):
    def __init__(self, gain_condition_generator: Callable[[Card], Callable[[Card], bool]]):
        super().__init__()
        self.gain_condition_generator = gain_condition_generator

    async def apply(self, game, player=None, *args, **kwargs) -> Any:
        trashed_card = await game.apply_effect(TrashFromHand(), player, *args, **kwargs)
        max_cost = trashed_card.cost + 3
        condition = self.gain_condition_generator(trashed_card)
        piles_allowed_to_gain_from = game.supply.get_pile_names_by_condition(condition)
        gained_card = await game.apply_effect(
            GainCardsToHand(amount=1, cost=(0, max_cost), allowed_pile_names=piles_allowed_to_gain_from), player, *args,
            **kwargs)
        return gained_card
