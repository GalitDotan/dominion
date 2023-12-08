from abc import ABC
from typing import Any, Optional

NULL_CHOICE: int = -1


class Options(ABC):
    """
    Represents a decision a player has to make.
    """

    def __init__(self, options: list[Any], min_choices_allowed: int, max_choices_allowed: int,
                 question: str = "What do you choose?"):
        self.question: str = question
        self.options: list[Any] = options
        self.decided: bool = False
        self.indexes_chosen: int | list[int] = []
        self._decisions: Optional[list[Any]] = None
        self.min_choices_allowed: int = min_choices_allowed
        self.max_choices_allowed: int = max_choices_allowed

    def __repr__(self):
        """
        Returns a string of the options
        """
        formatted_options = f'\r\n'.join([f'{i}. {option}' for i, option in enumerate(self.options, start=1)])
        return f'{self.question}\r\n{formatted_options}\r\n>> '

    @property
    def decision(self) -> Any | list[Any]:
        if not self.decided:
            raise Exception("Decisions were not yet made")
        if len(self._decisions) == 1:
            return self._decisions[0]
        return self._decisions.copy()

    def decide(self, choices: list[int] | int):
        """
        Make a decision.

        Param:
            choices: The index of the option (indexes start at 1)

        Raises:
             ValueError: if invalid choice
        """
        if not self.is_valid_choice(choices):
            raise ValueError(f'{choices} is not a valid choice.\r\n{self}')
        if type(choices) is int:
            if choices == NULL_CHOICE:
                choices = []
            else:
                choices = [choices]
        self._decisions = choices
        self.indexes_chosen = choices
        self.decided = True

    def undo_decision(self):
        """
        Undo the choice.
        """
        self._decisions = []
        self.decided = False

    def is_valid_choice(self, choices: list[int] | int) -> bool:
        """
        Validate indexes of choices and number of choices.
        """
        if type(choices) is int:
            choice = choices
            if choice == NULL_CHOICE and self.min_choices_allowed == 0:
                return True
            return choice in range(1, len(self.options) + 1) and self.min_choices_allowed == 1
        for choice in choices:
            if choice not in range(1, len(self.options) + 1):
                return False
        return self.min_choices_allowed <= len(choices) <= self.max_choices_allowed


class ClientOptions(Options):
    """
    A decision that is generated on Client side.
    """
    pass


class ServerOptions(Options):
    """
    A decision that is generated on Server side.
    """

    async def request_decision(self, websocket):
        """
        Send the decision through the websocket and await valid response.
        If invalid - retry.
        """
        choices = await websocket.recv()  # TODO: not here...
        try:
            self.decide(choices)
        except ValueError:
            await self.request_decision(websocket)
