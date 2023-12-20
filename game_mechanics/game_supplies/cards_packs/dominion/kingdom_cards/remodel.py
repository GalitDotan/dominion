from typing import Callable

from game_mechanics.effects.trash_cards import TrashThenGain
from game_mechanics.game_supplies.base_card import BaseCard
from game_mechanics.game_supplies.card_type import CardType


def condition_generator(trashed_card) -> Callable[[BaseCard], bool]:
    return lambda card: card.cost <= trashed_card.cost + 2


class Remodel(BaseCard):
    """
    Trash a card
    Gain a card costing up to 2 more
    """

    def __init__(self):
        super().__init__(name='Remodel',
                         cost=4,
                         types=CardType.ACTION,
                         action_effects=[TrashThenGain(
                             gain_condition_generator=condition_generator)])
