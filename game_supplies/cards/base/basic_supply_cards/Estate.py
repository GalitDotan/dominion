from game_supplies.card_types.card import Victory


class Estate(Victory):
    def __init__(self):
        super().__init__(name='Estate', cost=2, vp=1)
