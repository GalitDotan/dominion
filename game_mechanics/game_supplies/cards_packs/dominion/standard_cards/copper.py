from game_mechanics.game_supplies.base_card import BaseCard
from game_mechanics.game_supplies.card_type import CardType


class Copper(BaseCard):
    def __init__(self):
        super().__init__(
            name='Copper',
            cost=0,
            types=[CardType.TREASURE],
            treasure_effects=[]

        )
