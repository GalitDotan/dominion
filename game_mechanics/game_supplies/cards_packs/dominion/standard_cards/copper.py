from game_mechanics.effects.treasure_effect import TreasureEffect
from game_mechanics.game_supplies.base_card import TreasureCard
from game_mechanics.game_supplies.card_type import CardType


class Copper(TreasureCard):
    def __init__(self):
        super().__init__(
            name='Copper',
            cost=0,
            types=[CardType.TREASURE],
            treasure_effects=[TreasureEffect(value=1)]
        )
