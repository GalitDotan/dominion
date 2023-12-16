from abc import ABC, abstractmethod

import game_mechanics.effects.game_stages.phase.action_phase as action_phase
import game_mechanics.effects.game_stages.phase.buy_phase as buy_phase
import game_mechanics.effects.game_stages.phase.cleanup_phase as cleanup_phase
import game_mechanics.effects.game_stages.phase.end_game_phase as end_game_phase
import game_mechanics.effects.game_stages.phase.night_phase as night_phase
from game_mechanics.effects.effect import Effect


class BaseCard(Effect, ABC):
    """
    A card in a game. Stats can be modified
    """

    def __init__(self, name: str, cost: int, is_reveled: bool = False,
                 actions: list[tuple[Effect]] = (), treasures: list[tuple[Effect]] = (),
                 night_effects: list[tuple[Effect]] = (), cleanup_effects: list[tuple[Effect]] = (),
                 end_game_effects: list[tuple[Effect]] = ()):
        super().__init__(name)
        self.cost: int = cost
        self.is_reveled: bool = is_reveled
        self.activation_by_phase: dict[type[
            action_phase.ActionPhase | buy_phase.BuyPhase | night_phase.NightPhase |
            cleanup_phase.CleanUpPhase | end_game_phase.EndGamePhase], list[tuple[Effect]]] = {
            action_phase.ActionPhase: actions,
            buy_phase.BuyPhase: treasures,
            night_phase.NightPhase: night_effects,
            cleanup_phase.CleanUpPhase: cleanup_effects,
            end_game_phase.EndGamePhase: end_game_effects
        }

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name

    def __lt__(self, other: 'BaseCard'):
        if self.cost < other.cost:
            return True
        if self.cost > other.cost:
            return False
        return self.name < other.name

    @property
    def card_type(self):
        return type(self)  # TODO: show all inherited types

    @abstractmethod
    def detailed_repr(self):
        raise NotImplemented

    def activate(self, game):
        pass
