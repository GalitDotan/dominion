from game_mechanics.card_structures.hand import Hand
from game_mechanics.card_structures.pile import Pile
from game_mechanics.card_structures.play_area import PlayArea
from game_mechanics.game_supplies.card_types.card import Card
from game_mechanics.game_supplies.card_types.victory_card import Victory
from game_mechanics.states.base_state import BasePlayerState
from game_mechanics.utils.utils import shuffle_copy


class PlayerState(BasePlayerState):
    """
    The current state of the game elements of the curr_player:
        1. The Deck (all the cards he owns)
        2. The Hand
        3. The DiscardCard Pile
        4. The Draw Pile
        5. Different mats
    """

    def __init__(self, cards: list[Card], non_card_vp: int = 0):
        self._all_cards: list[Card] = cards.copy()  # all cards the curr_player has

        # curr_player's card structures
        self.draw_pile: Pile = Pile(name='Draw Pile', is_visible=False, cards=shuffle_copy(cards))
        self.discard_pile = Pile(name='DiscardCard Pile', is_visible=True)
        self.hand: Hand = Hand()
        self.play_area: PlayArea = PlayArea()

        # stats
        self._non_card_vp = non_card_vp  # All VP that does not come from cards

    def __repr__(self):
        return f"[{self.victory_points} VP]: {self.hand}, {self.draw_pile}, {self.discard_pile}"

    @property
    def victory_points(self) -> int:
        """
        Calculate the victory points by Player's cards and other places.

        Returns:
            Sum of victory points.
        """
        vp = self._non_card_vp
        for card in self._all_cards:
            if isinstance(card, Victory):
                vp += card.victory_points
        return vp

    def detailed_repr(self):
        return f"[{self.victory_points} VP]: {self.hand.detailed_repr()}{self.draw_pile.detailed_repr()}" \
               f"{self.discard_pile.detailed_repr()}"

    def get_cards_alphabetically(self) -> list[Card]:
        return sorted(self._all_cards, key=lambda x: x.name)

    def get_cards_by_value(self) -> list[Card]:
        return sorted(self._all_cards, key=lambda x: x.value)
