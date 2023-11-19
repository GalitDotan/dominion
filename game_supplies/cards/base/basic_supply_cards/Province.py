from game_supplies.card_types.victory_card import Victory


class Province(Victory):
    def __init__(self):
        super().__init__(name='Province', cost=8, vp=6)
