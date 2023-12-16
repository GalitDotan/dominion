from game_mechanics.game_supplies.card_types.action_card import ActionCard


class Remodel(ActionCard):
    def __init__(self):
        super().__init__(name='Remodel',
                         cost=4,
                         actions=[])
