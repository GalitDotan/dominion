from game_mechanics.effects.gain_cards import GainCardsDecision
from game_mechanics.game_supplies.base_card import CardObject
from game_mechanics.game_supplies.card_type import CardType


class Workshop(CardObject):
    """
    Gain a card costing up to 4 coins
    """

    def __init__(self):
        super().__init__(name='Workshop',
                         cost=3,
                         types=CardType.ACTION,
                         action_effects=[GainCardsDecision(amount=1, cost=(0, 4))])
