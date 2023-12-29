from typing import Optional

from game_mechanics.card_structures.hand import Hand
from game_mechanics.card_structures.pile import Pile
from game_mechanics.card_structures.play_area import PlayArea
from game_mechanics.game_supplies.base_card import CardObject
from game_mechanics.player.player_turn_state import PlayerTurnStats
from utils.name_generator import generate_player_name


class Player:
    """
    The current state of the game elements of the curr_player:
        1. The Deck (all the cards he owns)
        2. The Hand
        3. The DiscardCard Pile
        4. The Draw Pile
        5. Different mats
    """

    def __init__(self, name: str, game, non_card_vp: int = 0):
        self.name = name if name else generate_player_name()
        self.game = game

        self._all_cards: list[CardObject] = []  # all cards the player has

        # curr_player's card structures
        self.draw_pile: Pile = Pile(name='Draw Pile', is_visible=False)
        self.discard_pile = Pile(name='DiscardCard Pile', is_visible=True)
        self.hand: Hand = Hand()
        self.play_area: PlayArea = PlayArea()

        # All VP that does not come from cards + all victory cards that were already calculated
        self.achieved_victory_points = non_card_vp

        self.turns_played = 0
        self.turn_stats: Optional[PlayerTurnStats] = None  # this would be initiated every turn

        self._all_card_structures = (self.draw_pile, self.discard_pile, self.hand, self.play_area)

    def __repr__(self):
        return f'{self.name}[{self.estimate_victory_points} VP]: {self.hand}, {self.draw_pile}, {self.discard_pile}'

    def __lt__(self, other: "Player"):  # is self losing to other
        # return self.victory_points < other.victory_points or (
        #        self.victory_points == other.victory_points and self.turns_played >= other.turns_played)
        pass

    def __eq__(self, other: "Player"):
        # return self.victory_points == other.victory_points
        pass

    def __gt__(self, other: "Player"):  # is self winning other
        # return self.victory_points > other.victory_points or (
        #        self.victory_points == other.victory_points and self.turns_played < other.turns_played)
        pass

    @property
    def cards_amounts(self) -> dict[CardObject, int]:
        card_counter_dict: dict[CardObject, int] = {}
        for cars_structure in self._all_card_structures:
            for card, cnt in cars_structure.cards_dict.items():
                card_counter_dict[card] = card_counter_dict.get(card, 0) + cnt
        return card_counter_dict

    @property
    def estimate_victory_points(self) -> int:
        """
        Calculate the victory points by Player's cards and other places.

        Returns:
            Sum of victory points.
        """
        vp = self.achieved_victory_points
        for card, cnt in self.cards_amounts.items():
            vp += card.estimate_vp_worth(self.game) * cnt
        return vp

    def detailed_repr(self):
        return f"{self.name}[{self.estimate_victory_points} VP]: " \
               f"{self.hand.detailed_repr()}{self.draw_pile.detailed_repr()}" \
               f"{self.discard_pile.detailed_repr()}"

    def get_cards_alphabetically(self) -> list[CardObject]:
        return sorted(self._all_cards, key=lambda x: x.name)

    def get_cards_by_value(self) -> list[CardObject]:
        return sorted(self._all_cards, key=lambda x: x.value)

    def gain_card(self, card: CardObject):
        self._all_cards.append(card)

    def remove_cards(self, cards: CardObject | list[CardObject]):
        cards = (cards,) if type(cards) is CardObject else cards
        for card in cards:
            self._all_cards.remove(card)
