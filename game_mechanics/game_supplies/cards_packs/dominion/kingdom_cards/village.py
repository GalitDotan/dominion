from game_mechanics.game_supplies.card_types.action_card import ActionCard


class Village(ActionCard):
    def __init__(self):
        super().__init__(name='Village',
                         cost=3,
                         actions=[])
