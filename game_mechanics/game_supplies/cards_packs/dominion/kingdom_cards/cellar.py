from game_mechanics.effects.discard_then_draw import DiscardThenDraw
from game_mechanics.game_supplies.base_card import Card
from game_mechanics.game_supplies.card_type import CardType


class Cellar(Card):
    def __init__(self):
        super().__init__(name='Cellar',
                         cost=2,
                         types=CardType.ACTION,
                         action_effects=[DiscardThenDraw()])
