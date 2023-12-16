from game_mechanics.game_supplies.card_types.victory_card import VictoryCard


class Province(VictoryCard):
    def __init__(self):
        super().__init__(name='Province', cost=8, vp=6)
