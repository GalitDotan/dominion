from game_mechanics.effects.vp_effect import VPEffect, VPEffectKwargs
from game_mechanics.game_supplies.base_card import BaseCard
from game_mechanics.game_supplies.card_type import CardType


class Province(BaseCard):
    def __init__(self):
        super().__init__(
            name='Province',
            cost=8,
            types=CardType.VICTORY,
            end_game_effects=[(VPEffect, VPEffectKwargs(value=6))]
        )
