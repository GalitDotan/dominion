from abc import ABC
from typing import Optional

import game_mechanics.effects.game_stages.phase.action_phase as action_phase
import game_mechanics.effects.game_stages.phase.buy_phase as buy_phase
import game_mechanics.effects.game_stages.phase.cleanup_phase as cleanup_phase
import game_mechanics.effects.game_stages.phase.end_game_phase as end_game_phase
import game_mechanics.effects.game_stages.phase.night_phase as night_phase
from game_mechanics.effects.effect import Effect
from game_mechanics.game_supplies.card_type import CardType


class VPEffect(Effect):
    def activate(self, game):
        pass

    def estimate(self, game):
        pass


class BaseCard(Effect, ABC):
    """
    A card in a game. Stats can be modified
    """

    def __init__(self, name: str,
                 types: CardType | list[CardType],
                 cost: int,
                 action_effects: Optional[list[Effect | tuple[Effect]]] = (),
                 treasure_effects: Optional[list[Effect | tuple[Effect]]] = (),
                 night_effects: Optional[list[Effect | tuple[Effect]]] = (),
                 cleanup_effects: Optional[list[Effect | tuple[Effect]]] = (),
                 end_game_effects: Optional[list[Effect | tuple[Effect]]] = ()):
        super().__init__(name)
        self._cost: int = cost
        self._types: list[CardType] = types if type(types) is list else [types]
        self._effects_by_phase: dict[type[
            action_phase.ActionPhase | buy_phase.BuyPhase | night_phase.NightPhase |
            cleanup_phase.CleanUpPhase | end_game_phase.EndGamePhase], list[Effect | tuple[Effect]]] = {
            action_phase.ActionPhase: action_effects,
            buy_phase.BuyPhase: treasure_effects,
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
    def cost(self) -> int:
        return self._cost

    @property
    def types(self) -> list[CardType]:
        return self._types.copy()

    def effects_to_activate(self, game) -> list[Effect | tuple[Effect]]:
        phase = game.curr_phase
        if not phase:
            return []
        return self._effects_by_phase[phase]

    def activate(self, game):
        for effect in self.effects_to_activate(game):
            effect.activate(game)

    def estimate_vp_worth(self, game):
        vp_effects = self._effects_by_phase.get(end_game_phase.EndGamePhase)
        vps = 0
        for effect in vp_effects:
            effect: VPEffect
            vps += effect.estimate(game)
