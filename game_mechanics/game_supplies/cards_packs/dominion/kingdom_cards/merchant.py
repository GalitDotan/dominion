from game_mechanics.effects.game_stages.phase.cleanup_phase import CleanUpPhase
from game_mechanics.effects.increase_stats import IncStats
from game_mechanics.effects.move_cards.draw_num_cards import DrawNum
from game_mechanics.effects.reactions.on_effect_reaction import OnEffectReaction
from game_mechanics.effects.treasure_effect import TreasureEffect
from game_mechanics.game_supplies.base_card import BaseCard
from game_mechanics.game_supplies.card_type import CardType
from game_mechanics.game_supplies.cards_packs.dominion.standard_cards import Silver


# TODO: test conditions

def is_played_card_is_silver(card, *args, **kwargs):
    return type(card) is Silver


def is_cleanup_phase(phase, *args, **kwargs):
    return type(phase) is CleanUpPhase


class Merchant(BaseCard):
    """
    +1 Card
    +1 Action
    The first time you play a Silver this turn, +1 coin
    """

    def __init__(self):
        super().__init__(name='Merchant',
                         cost=3,
                         types=CardType.ACTION,
                         action_effects=[DrawNum(num=1),
                                         IncStats(actions=1),
                                         OnEffectReaction(react_on_effect=TreasureEffect,
                                                          apply_times=1,
                                                          apply_condition=is_played_card_is_silver,
                                                          remove_condition=is_cleanup_phase)])
