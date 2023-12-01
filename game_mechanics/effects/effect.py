from abc import abstractmethod, ABC
from typing import Optional

from base_decision import BaseDecision
from game_mechanics.states.game_state import GameState


class Effect(ABC):
    """
    An element that changes the state of the game/turn when applied.
    """

    def __init__(self, followup_effect: Optional['Effect'] = None):
        self.followup_effect = followup_effect

    def activate(self, game_state: GameState, decision: BaseDecision):
        """
        Activate this effect according to a player's decision.

        Params:
            game_state: The current state of the game.
            decision: The decision of the player.
        """
        decision.wait_for_decision()
        result: Optional[BaseDecision] = self.on_activation(game_state, decision)
        if self.followup_effect:
            self.followup_effect.activate(game_state, result)

    @abstractmethod
    def on_activation(self, game_state: GameState, decision: BaseDecision):
        pass
