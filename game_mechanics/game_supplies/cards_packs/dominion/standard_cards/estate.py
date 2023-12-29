from game_mechanics.effects.vp_effect import VPEffect
from game_mechanics.game_supplies.base_card import CardObject
from game_mechanics.game_supplies.card_type import CardType


class Estate(CardObject):
    def __init__(self):
        super().__init__(
            name='Estate',
            cost=2,
            types=CardType.VICTORY,
            end_game_effects=[VPEffect(value=1)]
        )
