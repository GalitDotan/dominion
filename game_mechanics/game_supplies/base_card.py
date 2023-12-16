from abc import ABC
from typing import Optional

import game_mechanics.effects.game_stages.phase.action_phase as action_phase
import game_mechanics.effects.game_stages.phase.buy_phase as buy_phase
import game_mechanics.effects.game_stages.phase.cleanup_phase as cleanup_phase
import game_mechanics.effects.game_stages.phase.end_game_phase as end_game_phase
import game_mechanics.effects.game_stages.phase.night_phase as night_phase
from game_mechanics.effects.effect import Effect, VPEffect
from game_mechanics.game_supplies.card_type import CardType


class BaseCard(ABC):
    """
    A card in a game. Stats can be modified
    """

    def __init__(self,
                 name: str,
                 types: CardType | list[CardType],
                 cost: int,
                 action_effects: Optional[list[type[Effect] | tuple[type[Effect]]]] = (),
                 treasure_effects: Optional[list[type[Effect] | tuple[type[Effect]]]] = (),
                 night_effects: Optional[list[type[Effect] | tuple[type[Effect]]]] = (),
                 cleanup_effects: Optional[list[type[Effect] | tuple[type[Effect]]]] = (),
                 end_game_effects: Optional[list[type[Effect] | tuple[type[Effect]]]] = ()):
        self.name = name
        self._cost: int = cost
        self._types: list[CardType] = types if type(types) is list else [types]
        self._effects_by_phase: dict[type[
            action_phase.ActionPhase | buy_phase.BuyPhase | night_phase.NightPhase |
            cleanup_phase.CleanUpPhase | end_game_phase.EndGamePhase], list[type[Effect] | tuple[type[Effect]]]] = {
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
        """
        All types of the card.
        """
        return self._types.copy()

    def is_playable(self, phase):
        return len(self._effects_by_phase.get(phase, [])) > 0

    def effects_to_activate(self, game, phase=None) -> list[type[Effect] | tuple[type[Effect]]]:
        """
        Get the types of effects to activate by phase.
        Default phase - current.
        """
        phase = phase if phase else game.curr_phase
        return [t if type(t) is tuple else (t,) for t in self._effects_by_phase.get(phase, [])]

    def play(self, game):
        for effect in self.effects_to_activate(game):
            game.apply_effect(effect())

    def estimate_vp_worth(self, game):
        vp_effects = self._effects_by_phase.get(end_game_phase.EndGamePhase)
        vps = 0
        for effect in vp_effects:
            effect: VPEffect
            vps += effect.estimate(game)
