from game_mechanics.game_supplies.card_types.base_card import BaseCard


class TreasureCard(BaseCard):

    def __init__(self, name: str, cost: int, coins: int, automatic_play: bool = True, *args, **kwargs):
        super().__init__(name, cost, *args, **kwargs)
        self.coins = coins
        self.automatic_play: bool = automatic_play

    def detailed_repr(self):
        return f"""
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        ### {self.name} ###

        # Type: {self.card_type}
        # Cost: {self.cost}

        ~ {self.coins} ~

        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        """

    def play(self):
        return self.coins
