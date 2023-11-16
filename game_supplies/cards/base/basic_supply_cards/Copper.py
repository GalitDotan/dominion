from game_supplies.card_types.card import Treasure


class Copper(Treasure):
    def __init__(self):
        super().__init__(name='Copper', cost=0, coins=1)
