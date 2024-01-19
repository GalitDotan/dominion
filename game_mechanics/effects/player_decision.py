from typing import Any

from game_mechanics.effects.effect import Effect


class PlayerCheckboxChoice(Effect):
    """
    Choosing numbered options from a list of options.
    For example: '1 3 4'
    """
    NONE_CHOICE = 'none'
    DELIMITER = ''

    def __init__(self, choices: list[Any], header: str = "Please choose from", allow_none_noice: bool = True):
        super().__init__()
        self.header = header
        self.choices: list[Any] = choices if choices else []
        if allow_none_noice:
            self.choices.append(PlayerCheckboxChoice.NONE_CHOICE)

    async def apply(self, game, player=None, *args, **kwargs) -> Any:
        options = '\r\n'.join([f'{i}. {str(choice)}' for i, choice in enumerate(self.choices, start=1)])
        message = f'{self.header}: {options}'
        await game.send_personal_message(message, player)
        response = await game.receive_text(player)
        print(f'Player answered: "{response}"')
        return self.format_result(response)

    def format_result(self, response: str):
        try:
            choice = int(response)
            result = self.choices[choice]
            if result == PlayerCheckboxChoice.NONE_CHOICE:
                return []
            return [result]
        except ValueError:
            chosen_choices = [int(i) - 1 for i in PlayerCheckboxChoice.DELIMITER.split(response)]
            return [self.choices[i] for i in chosen_choices]


class PlayerBooleanChoice(PlayerCheckboxChoice):
    """
    Asking a player for a Yes/No choice.
    """
    YES = 'yes'
    NO = 'no'

    def __init__(self, header: str = "Please choose from"):
        super().__init__(choices=[PlayerBooleanChoice.YES, PlayerBooleanChoice.NO], header=header,
                         allow_none_noice=False)

    def format_result(self, response: str):
        result = super().format_result(response)
        if result[0] == PlayerBooleanChoice.YES:
            return True
        return False


class PlayerChoiceFromRange(PlayerCheckboxChoice):
    """
    Asking a player to choose a number from a given range.
    """

    def __init__(self, option_range: tuple[int, int], header: str = "Please choose from"):
        super().__init__(choices=list(range(option_range[0], option_range[1] + 1)),
                         header=header,
                         allow_none_noice=False)
