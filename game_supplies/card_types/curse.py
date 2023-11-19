from game_supplies.card_types.card import Card


class Curse(Card):
    def __init__(self, name: str = 'Curse', cost: int = 0):
        super().__init__(name, cost)
        self.vp = -1

    def detailed_repr(self):
        return f"""
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        ### Curse ###

        # Type: {self.card_type}
        # Cost: {self.cost}

        ~ {self.vp} VP ~

        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        """
