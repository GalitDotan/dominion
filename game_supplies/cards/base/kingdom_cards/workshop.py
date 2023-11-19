from game_supplies.card_types.action_card import Action


class Workshop(Action):
    def __init__(self):
        super().__init__(name='Workshop',
                         cost=3,
                         commands=[])
