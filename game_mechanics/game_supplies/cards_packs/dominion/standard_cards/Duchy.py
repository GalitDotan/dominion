from game_mechanics.game_supplies.card_types.victory_card import VictoryCard


class Duchy(VictoryCard):
    def __init__(self):
        super().__init__(name='Duchy', cost=5, vp=3)
