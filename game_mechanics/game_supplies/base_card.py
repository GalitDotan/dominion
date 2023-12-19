from abc import ABC

import game_mechanics.effects.game_stages.phase.action_phase as action_phase
import game_mechanics.effects.game_stages.phase.buy_phase as buy_phase
import game_mechanics.effects.game_stages.phase.cleanup_phase as cleanup_phase
import game_mechanics.effects.game_stages.phase.end_game_phase as end_game_phase
import game_mechanics.effects.game_stages.phase.night_phase as night_phase
from game_mechanics.effects.effect import Effect
from game_mechanics.effects.vp_effect import VPEffect
from game_mechanics.game_supplies.card_type import CardType


class BaseCard(ABC):
    """
    A card in a game. Stats can be modified
    """

    def __init__(self,
                 name: str,
                 types: CardType | list[CardType],
                 cost: int,
                 action_effects: list[Effect] = (),
                 treasure_effects: list[Effect] = (),
                 night_effects: list[Effect] = (),
                 cleanup_effects: list[Effect] = (),
                 end_game_effects: list[Effect] = ()):
        self.name = name
        self._cost: int = cost
        self._types: list[CardType] = types if type(types) is list else [types]
        self._effects_by_phase: dict[type[
            action_phase.ActionPhase | buy_phase.BuyPhaseTreasures | night_phase.NightPhase |
            cleanup_phase.CleanUpPhase | end_game_phase.EndGamePhase], list[Effect]] = {
            action_phase.ActionPhase: action_effects,
            buy_phase.BuyPhaseTreasures: treasure_effects,
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

    def effects_to_activate(self, game, phase=None) -> list[Effect]:
        """
        Get the types of effects to activate by phase.
        Default phase - current.
        """
        phase = phase if phase else game.curr_phase
        return [t for t in self._effects_by_phase.get(phase, [])]

    def play(self, game):
        """
        Apply all the effect of the card for the current phase.
        """
        for effect, model in self.effects_to_activate(game):
            game.apply_effect(effect)

    def estimate_vp_worth(self, game):
        """
        Estimate the VP this card is worth.
        """
        vp_effects = self._effects_by_phase.get(end_game_phase.EndGamePhase)
        vps = 0
        for effect in vp_effects:
            effect: VPEffect
            vps += effect.estimate(game)
