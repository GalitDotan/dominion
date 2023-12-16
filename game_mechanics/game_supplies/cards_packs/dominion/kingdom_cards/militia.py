from game_mechanics.game_supplies.card_types.action_card import ActionCard


class Militia(ActionCard):
    def __init__(self):
        super().__init__(name='Militia',
                         cost=4,
                         actions=[])
