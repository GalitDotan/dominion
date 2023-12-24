from game_mechanics.effects.attack_effect import AttackEffect
from game_mechanics.effects.draw_cards import DrawCards
from game_mechanics.effects.game_stages.phase.cleanup_phase import CleanUpPhase
from game_mechanics.game_supplies.base_card import ReactionCard
from game_mechanics.game_supplies.card_type import CardType


def is_cleanup_phase(phase, *args, **kwargs):
    return type(phase) is CleanUpPhase


def is_in_hand():
    return True


class Moat(ReactionCard):
    """
    +2 cards
    _______________
    If another player_name plays an attack....
    """

    def __init__(self):
        super().__init__(name='Moat',
                         cost=2,
                         types=CardType.ACTION,
                         action_effects=[DrawCards(amount=2)],
                         react_on_effect=AttackEffect,
                         apply_times=1,
                         apply_condition=is_in_hand,
                         remove_condition=is_cleanup_phase)
