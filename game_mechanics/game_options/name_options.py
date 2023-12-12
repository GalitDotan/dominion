from game_mechanics.game_options.game_options import GameOptions


class CheckboxOptions(GameOptions):
    """
    Choosing an option from a list
    """

    def __init__(self, options: list[str], min_choices_allowed: int, max_choices_allowed: int):
        super().__init__(options, min_choices_allowed, max_choices_allowed)
        self.chosen_cards: list[str] = []

    def decide(self, choices: list[int] | int):
        super().decide(choices)
        self.chosen_cards = self._chosen_options
