from game_mechanics.game_supplies.card_types.treasure_card import TreasureCard


class Gold(TreasureCard):
    def __init__(self):
        super().__init__(name='Gold', cost=6, coins=3)
