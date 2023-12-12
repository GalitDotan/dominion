from abc import abstractmethod, ABC
from typing import Optional

from game_mechanics.game_options.game_options import GameOptions
from options import Options


class Effect(ABC):
    """
    An element that changes the state of the game/turn when applied.
    """

    def __init__(self, followup_effect: Optional['Effect'] = None):
        self.followup_effect = followup_effect

    @abstractmethod
    def __repr__(self):
        pass

    def activate(self, game_state, options: GameOptions, on_player: Optional[str] = None):
        """
        Activate this effect according to a player's decision.

        Params:
            game_state: The current state of the game.
            decision: The decision of the player.
            on_player: on which player to apply the effect. Default - current player.
        """
        if not on_player:
            on_player = game_state.curr_player
        waiting_reactions = []
        options.request_decision()  # TODO: fix
        result: Optional[GameOptions] = self.on_activation(game_state, options, on_player)
        if self.followup_effect:
            self.followup_effect.activate(game_state, result)

    @abstractmethod
    def on_activation(self, game_state, decision: Options, player: str):
        pass
