from game_mechanics.effects.vp_effect import VPEffect
from game_mechanics.game_supplies.base_card import Card
from game_mechanics.game_supplies.card_type import CardType


class Province(Card):
    def __init__(self):
        super().__init__(
            name='Province',
            cost=8,
            types=CardType.VICTORY,
            end_game_effects=[VPEffect(value=6)]
        )
