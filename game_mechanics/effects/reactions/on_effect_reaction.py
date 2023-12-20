from abc import ABC, abstractmethod
from typing import Optional, Any, final, Callable

from game_mechanics.effects.effect import Effect


class Reaction(Effect, ABC):
    def __init__(self, react_on_effect: type[Effect], apply_times: Optional[int] = None,
                 apply_condition: Optional[Callable] = None, remove_condition: Optional[Callable] = None):
        super().__init__()
        self.react_on_effect: type[Effect] = react_on_effect
        self.apply_times: Optional[int] = apply_times
        self.count_activations = 0
        self.apply_condition = apply_condition
        self.remove_condition = remove_condition

    def should_react(self, activated_effect: Effect, game, player=None, *args, **kwargs) -> bool:
        return type(activated_effect) is self.react_on_effect and self.apply_condition(activated_effect, game, player,
                                                                                       *args, **kwargs)

    def should_remove(self, game, player=None, *args, **kwargs) -> bool:
        return self.remove_condition(game, player, *args, **kwargs)

    @final
    def apply(self, game, player=None, *args, **kwargs) -> Any:
        self.count_activations += 1
        self.apply_activation(game, player, *args, **kwargs)
        if self.count_activations == self.apply_times:
            game.remove_waiting_reaction(self)

    @abstractmethod
    def apply_activation(self, game, player=None, *args, **kwargs) -> Any:
        pass
