from game_mechanics.game_supplies.card_types.action_card import Action


class Merchant(Action):
    def __init__(self):
        super().__init__(name='Merchant',
                         cost=3,
                         actions=[])
