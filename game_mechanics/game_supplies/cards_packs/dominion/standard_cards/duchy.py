from game_mechanics.effects.vp_effect import VPEffect
from game_mechanics.game_supplies.base_card import TreasureCard
from game_mechanics.game_supplies.card_type import CardType


class Duchy(TreasureCard):
    def __init__(self):
        super().__init__(
            name='Duchy',
            cost=5,
            types=CardType.VICTORY,
            end_game_effects=[VPEffect(value=3)]
        )
