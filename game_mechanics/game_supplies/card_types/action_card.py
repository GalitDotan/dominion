from game_mechanics.effects.effect import Effect
from game_mechanics.game_supplies.card_types.base_card import BaseCard


class ActionCard(BaseCard):

    def __init__(self, name: str, cost: int, actions: list[Effect]):
        super().__init__(name, cost)
        self.actions: list = actions

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
        return "\n".join([str(c) for c in self.actions])
