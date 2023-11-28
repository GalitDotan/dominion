from game_mechanics.game_supplies.card_types.card import Card


class Action(Card):

    def __init__(self, name: str, cost: int, commands: list):
        super().__init__(name, cost)
        self.commands: list = commands

    def detailed_repr(self):
        return f"""
                ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                ### {self.name} ###

                # Type: {self.card_type}
                # Cost: {self.cost}

                {self.description}

                ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                """

    @property
    def description(self):
        return "\n".join([str(c) for c in self.commands])
