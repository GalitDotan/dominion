from game_mechanics.game_supplies.base_card import BaseCard
from game_mechanics.game_supplies.card_type import CardType


class Silver(BaseCard):
    def __init__(self):
        super().__init__(
            name='Silver',
            cost=3,
            types=[CardType.TREASURE],
            treasure_effects=[]

        )
