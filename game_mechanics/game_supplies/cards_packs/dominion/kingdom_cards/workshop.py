from game_mechanics.effects.gain_cards import GainCardsToDiscard
from game_mechanics.game_supplies.base_card import Card
from game_mechanics.game_supplies.card_type import CardType


class Workshop(Card):
    """
    Gain a card costing up to 4 coins
    """

    def __init__(self):
        super().__init__(name='Workshop',
                         cost=3,
                         types=CardType.ACTION,
                         action_effects=[GainCardsToDiscard(amount=1, cost=(0, 4))])
