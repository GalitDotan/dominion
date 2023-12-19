from game_mechanics.effects.vp_effect import VPEffect
from game_mechanics.game_supplies.base_card import BaseCard
from game_mechanics.game_supplies.card_type import CardType


class Curse(BaseCard):
    def __init__(self):
        super().__init__(
            name='Curse',
            cost=0,
            types=CardType.CURSE,
            end_game_effects=[VPEffect(value=-1)]
        )
