from game_mechanics.effects.draw_cards import DrawCards
from game_mechanics.game_supplies.base_card import Card
from game_mechanics.game_supplies.card_type import CardType


class Smithy(Card):
    def __init__(self):
        super().__init__(name='Smithy',
                         cost=4,
                         types=CardType.ACTION,
                         action_effects=[DrawCards(amount=3)])
