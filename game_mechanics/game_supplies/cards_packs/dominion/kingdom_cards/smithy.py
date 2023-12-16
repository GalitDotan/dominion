from game_mechanics.game_supplies.base_card import BaseCard
from game_mechanics.game_supplies.card_type import CardType


class Smithy(BaseCard):
    def __init__(self):
        super().__init__(name='Smithy',
                         cost=4,
                         types=CardType.ACTION,
                         action_effects=[])
