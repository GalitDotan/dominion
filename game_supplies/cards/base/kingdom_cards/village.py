from game_supplies.card_types.card import Action


class Village(Action):
    def __init__(self):
        super().__init__(name='Village',
                         cost=3,
                         commands=[])
