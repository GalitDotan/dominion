from game_supplies.card_types.action_card import Action


class Market(Action):
    def __init__(self):
        super().__init__(name='Market',
                         cost=5,
                         commands=[])
