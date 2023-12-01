from abc import ABC

from base_decision import BaseDecision
from game_mechanics.game_supplies.card_types.card import Card


class GameDecision(BaseDecision):
    """
    Represents a decision a curr_player has to make.
    """
    pass


class EmptyDecision(GameDecision):
    """
    An "Empty BaseDecision" is a dummy decision (a curr_player does not have a decision to make.
    """
    pass


class NumDecision(GameDecision):
    """
    Deciding on a number from given range.
    """

    def __init__(self, default: int = 0):
        super().__init__()
        self.num = default


class CardsDecision(GameDecision, ABC):
    def __init__(self, cards: list[Card]):
        super().__init__()
        self.cards = cards


class DiscardDecision(CardsDecision):
    """
    Deciding on which cards to discard.
    """

    def __init__(self, cards: list[Card]):
        super().__init__(cards)


class TrashDecision(CardsDecision):
    """
    Deciding on which cards to trash.
    """

    def __init__(self, cards: list[Card]):
        super().__init__(cards)
