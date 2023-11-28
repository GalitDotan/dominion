from game_mechanics.game_supplies.card_types.action_card import Action


class Militia(Action):
    def __init__(self):
        super().__init__(name='Militia',
                         cost=4,
                         commands=[])
