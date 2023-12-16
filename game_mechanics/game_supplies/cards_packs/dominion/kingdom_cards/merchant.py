from game_mechanics.game_supplies.base_card import BaseCard
from game_mechanics.game_supplies.card_type import CardType


class Merchant(BaseCard):
    def __init__(self):
        super().__init__(name='Merchant',
                         cost=3,
                         types=CardType.ACTION,
                         action_effects=[])
