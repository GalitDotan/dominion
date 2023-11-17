from game_supplies.card_types.card import Action


class Smithy(Action):
    def __init__(self):
        super().__init__(name='Smithy',
                         cost=4,
                         commands=[])
