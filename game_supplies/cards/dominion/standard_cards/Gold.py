from game_supplies.card_types.treasure_card import Treasure


class Gold(Treasure):
    def __init__(self):
        super().__init__(name='Gold', cost=6, coins=3)
