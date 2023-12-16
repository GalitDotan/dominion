from game_mechanics.game_supplies.card_types.action_card import ActionCard


class Merchant(ActionCard):
    def __init__(self):
        super().__init__(name='Merchant',
                         cost=3,
                         actions=[])
