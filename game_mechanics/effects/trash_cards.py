from typing import Any, Callable

from game_mechanics.effects.effect import Effect
from game_mechanics.effects.gain_cards import GainCardsDecision, GainCard, GainCardToDiscard
from game_mechanics.effects.player_decision import PlayerCheckboxChoice
from game_mechanics.game_supplies.base_card import CardObject


class TrashFromHand(Effect):
    async def apply(self, game, player=None, *args, **kwargs) -> Any:
        treasure = await game.apply_effect(PlayerCheckboxChoice(player.hand.cards), player)
        player.hand.remove(treasure)
        player.remove_card(treasure)
        game.trash.append(treasure)
        return treasure


class TrashThenGain(Effect):
    def __init__(self, gain_condition_generator: Callable[[CardObject], Callable[[CardObject], bool]],
                 gain_type: type[GainCard] = GainCardToDiscard):
        super().__init__()
        self.gain_condition_generator = gain_condition_generator
        self.gain_type = gain_type

    async def apply(self, game, player=None, *args, **kwargs) -> Any:
        trashed_card = await game.apply_effect(TrashFromHand(), player, *args, **kwargs)
        max_cost = trashed_card.cost + 3
        condition = self.gain_condition_generator(trashed_card)
        piles_allowed_to_gain_from = game.supply.get_non_empty_pile_names(condition)
        gained_card = await game.apply_effect(
            GainCardsDecision(gain_type=self.gain_type, amount=1, cost=(0, max_cost),
                              allowed_pile_names=piles_allowed_to_gain_from),
            player,
            *args,
            **kwargs)
        return gained_card
