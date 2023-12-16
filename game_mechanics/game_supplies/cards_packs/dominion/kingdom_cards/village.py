from game_mechanics.game_supplies.base_card import BaseCard
from game_mechanics.game_supplies.card_type import CardType


class Village(BaseCard):
    def __init__(self):
        super().__init__(name='Village',
                         cost=3,
                         types=CardType.ACTION,
                         action_effects=[])
