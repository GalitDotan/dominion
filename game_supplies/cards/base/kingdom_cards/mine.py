from game_supplies.card_types.card import Action


class Mine(Action):
    def __init__(self):
        super().__init__(name='Mine',
                         cost=5,
                         commands=[])
