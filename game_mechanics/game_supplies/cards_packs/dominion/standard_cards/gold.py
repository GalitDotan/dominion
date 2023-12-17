from game_mechanics.effects.treasure_effect import TreasureEffect, TreasureEffectKwargs
from game_mechanics.game_supplies.base_card import BaseCard
from game_mechanics.game_supplies.card_type import CardType


class Gold(BaseCard):
    def __init__(self):
        super().__init__(
            name='Gold',
            cost=6,
            types=[CardType.TREASURE],
            treasure_effects=[(TreasureEffect, dict(TreasureEffectKwargs(value=3)))]
        )
