from game_mechanics.game_supplies.card_types.action_card import ActionCard


class Market(ActionCard):
    def __init__(self):
        super().__init__(name='Market',
                         cost=5,
                         actions=[])
