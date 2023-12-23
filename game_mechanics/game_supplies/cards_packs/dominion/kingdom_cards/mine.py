from game_mechanics.effects.trash_cards import TrashThenGain
from game_mechanics.game_supplies.base_card import Card
from game_mechanics.game_supplies.card_type import CardType


def condition_generator(trashed_card):
    return lambda card: card.cost <= trashed_card.cost + 3 and CardType.TREASURE in card.types()


class Mine(Card):
    """
    You may trash a treasure from your hand.
    Gain a treasure to your hand costing up to 3 Coins more.
    """

    def __init__(self):
        super().__init__(name='Mine',
                         cost=5,
                         types=CardType.ACTION,
                         action_effects=[TrashThenGain(
                             gain_condition_generator=condition_generator)])
