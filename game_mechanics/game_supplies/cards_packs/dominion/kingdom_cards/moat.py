from game_mechanics.game_supplies.card_types.action_card import Action


class Moat(Action):
    def __init__(self):
        super().__init__(name='Moat',
                         cost=2,
                         actions=[])
