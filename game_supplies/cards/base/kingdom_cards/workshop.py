from game_supplies.card_types.card import Action


class Workshop(Action):
    def __init__(self):
        super().__init__(name='Workshop',
                         cost=3,
                         commands=[])
