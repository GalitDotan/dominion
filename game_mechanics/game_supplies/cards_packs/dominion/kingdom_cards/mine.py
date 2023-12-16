from game_mechanics.game_supplies.card_types.action_card import ActionCard


class Mine(ActionCard):
    def __init__(self):
        super().__init__(name='Mine',
                         cost=5,
                         actions=[])
