from typing import Any

from game_mechanics.effects.effect import Effect


class PlayerDecision(Effect):
    NONE_CHOICE = 'none'

    def __init__(self, choices: list[Any], allow_none_noice: bool = True):
        super().__init__()
        self.choices: list[Any] = choices
        if allow_none_noice:
            self.choices.append(PlayerDecision.NONE_CHOICE)

    async def apply(self, game, player=None, *args, **kwargs) -> Any:
        options = '\r\n'.join([f'{i}. {str(choice)}' for i, choice in enumerate(self.choices, start=1)])
        message = f'Please choose from: {options}'
        await game.send_personal_message(message, player)
        response = game.receive_text
        chosen_choices = [int(i) - 1 for i in ' '.split(response)]
        result = [self.choices[i] for i in chosen_choices]
        self.format_result(result)
        return result

    def format_result(self, result: list[Any]):
        if result[-1] == PlayerDecision.NONE_CHOICE:
            result[-1] = None
        if len(result) == 1:
            return result[0]


class PlayerBooleanDecision(PlayerDecision):
    YES = 'yes'
    NO = 'no'

    def __init__(self):
        super().__init__(choices=['yes', 'no'], allow_none_noice=False)

    def format_result(self, result: list[Any]):
        if result[0] == PlayerBooleanDecision.YES:
            return True
        return False


class PlayerIntDecision(PlayerDecision):

    def __init__(self, option_range: tuple[int, int]):
        super().__init__(choices=list(range(option_range[0], option_range[1] + 1)), allow_none_noice=False)

    def format_result(self, result: list[Any]):
        return int(result[0])
