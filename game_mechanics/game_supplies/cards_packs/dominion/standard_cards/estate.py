from game_mechanics.effects.vp_effect import VPEffect, VPEffectKwargs
from game_mechanics.game_supplies.base_card import BaseCard
from game_mechanics.game_supplies.card_type import CardType


class Estate(BaseCard):
    def __init__(self):
        super().__init__(
            name='Estate',
            cost=2,
            types=CardType.VICTORY,
            end_game_effects=[(VPEffect, VPEffectKwargs(value=1))]
        )
