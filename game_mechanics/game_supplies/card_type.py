from enum import Enum

from card_types import *


class CardType(Enum):
    ACTION = ActionCard
    ATTACK = AttackCard
    CURSE = CurseCard
    DURATION = DurationCard
    NIGHT = NightCard
    REACTION = ReactionCard
    VICTORY = VictoryCard
