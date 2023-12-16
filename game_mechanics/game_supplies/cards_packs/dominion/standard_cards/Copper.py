from game_mechanics.game_supplies.card_types.treasure_card import TreasureCard


class Copper(TreasureCard):
    def __init__(self):
        super().__init__(name='Copper', cost=0, coins=1)
