from game_mechanics.game_supplies.base_card import BaseCard
from game_mechanics.game_supplies.card_type import CardType


class Cellar(BaseCard):
    def __init__(self):
        super().__init__(name='Cellar',
                         cost=2,
                         types=CardType.ACTION,
                         action_effects=[])
