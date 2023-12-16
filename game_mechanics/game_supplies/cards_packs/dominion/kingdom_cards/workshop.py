from game_mechanics.game_supplies.card_types.action_card import ActionCard


class Workshop(ActionCard):
    def __init__(self):
        super().__init__(name='Workshop',
                         cost=3,
                         actions=[])
