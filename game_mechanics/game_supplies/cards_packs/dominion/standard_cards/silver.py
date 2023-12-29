from game_mechanics.effects.treasure_effect import TreasureEffect
from game_mechanics.game_supplies.base_card import CardObject
from game_mechanics.game_supplies.card_type import CardType


class Silver(CardObject):
    def __init__(self):
        super().__init__(
            name='Silver',
            cost=3,
            types=[CardType.TREASURE],
            treasure_effects=[TreasureEffect(value=2)]
        )
