from game_mechanics.game_supplies.card_types.base_card import BaseCard


class VictoryCard(BaseCard):

    def __init__(self, name: str, cost: int, vp: int, *args, **kwargs):
        super().__init__(name=name, cost=cost, *args, **kwargs)
        self._vp: int = vp

    def detailed_repr(self):
        return f"""
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        ### {self.name} ###

        # Type: {self.card_type}
        # Cost: {self.cost}

        ~ {self._vp} VP ~

        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        """

    @property
    def victory_points(self):
        return self._vp
