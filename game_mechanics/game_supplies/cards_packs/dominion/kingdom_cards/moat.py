from game_mechanics.game_supplies.card_types.action_card import ActionCard


class Moat(ActionCard):
    def __init__(self):
        super().__init__(name='Moat',
                         cost=2,
                         actions=[])
