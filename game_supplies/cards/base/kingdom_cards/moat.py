from game_supplies.card_types.card import Action


class Moat(Action):
    def __init__(self):
        super().__init__(name='Moat',
                         cost=2,
                         commands=[])
