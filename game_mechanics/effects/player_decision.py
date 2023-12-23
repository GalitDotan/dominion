from typing import Any

from game_mechanics.effects.effect import Effect


class PlayerDecision(Effect):

    def __init__(self, choices: list[Any]):
        super().__init__()
        self.choices = choices

    async def apply(self, game, player=None, *args, **kwargs) -> Any:
        options = '\r\n'.join([f'{i}. {str(choice)}' for i, choice in enumerate(self.choices, start=1)])
        message = f'Please choose from: {options}'
        await game.send_personal_message(message, player)
        response = game.receive_text
        chosen_choices = [int(i) - 1 for i in ' '.split(response)]
        return [self.choices[i] for i in chosen_choices]
