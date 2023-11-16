from game_supplies.card_types.card import Treasure


class Silver(Treasure):
    def __init__(self):
        super().__init__(name='Silver', cost=3, coins=2)
