from game_mechanics.game_supplies.card_types.action_card import ActionCard


class Smithy(ActionCard):
    def __init__(self):
        super().__init__(name='Smithy',
                         cost=4,
                         actions=[])
