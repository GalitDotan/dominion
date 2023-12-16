from game_mechanics.game_supplies.base_card import BaseCard
from game_mechanics.game_supplies.card_type import CardType


class Moat(BaseCard):
    def __init__(self):
        super().__init__(name='Moat',
                         cost=2,
                         types=CardType.ACTION,
                         action_effects=[])
