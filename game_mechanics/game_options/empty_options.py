from game_mechanics.game_options.game_options import GameOptions


class EmptyOptions(GameOptions):
    """
    An "Empty Options" is a dummy decision (a curr_player does not have a decision to make.
    """

    def __init__(self):
        super().__init__(options=[], min_choices_allowed=0, max_choices_allowed=0)
