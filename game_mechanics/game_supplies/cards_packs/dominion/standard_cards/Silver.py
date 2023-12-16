from game_mechanics.game_supplies.card_types.treasure_card import TreasureCard


class Silver(TreasureCard):
    def __init__(self):
        super().__init__(name='Silver', cost=3, coins=2)
