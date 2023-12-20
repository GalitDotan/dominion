from typing import Optional

from game_mechanics.card_structures.hand import Hand
from game_mechanics.card_structures.pile import Pile
from game_mechanics.card_structures.play_area import PlayArea
from game_mechanics.game_supplies.base_card import BaseCard
from game_mechanics.player.player_turn_state import PlayerTurnStats
from game_mechanics.utils.utils import shuffle_copy
from utils.name_generator import generate_name


class Player:
    """
    The current state of the game elements of the curr_player:
        1. The Deck (all the cards he owns)
        2. The Hand
        3. The DiscardCard Pile
        4. The Draw Pile
        5. Different mats
    """

    def __init__(self, name: str, cards: list[BaseCard], non_card_vp: int = 0):
        self.name = name if name else generate_name()

        self._all_cards: list[BaseCard] = cards.copy()  # all cards the curr_player has

        # curr_player's card structures
        self.draw_pile: Pile = Pile(name='Draw Pile', is_visible=False, cards=shuffle_copy(cards))
        self.discard_pile = Pile(name='DiscardCard Pile', is_visible=True)
        self.hand: Hand = Hand()
        self.play_area: PlayArea = PlayArea()

        # All VP that does not come from cards + all victory cards that were already calculated
        self.achieved_victory_points = non_card_vp

        self.turns_played = 0
        self.turn_stats: Optional[PlayerTurnStats] = None  # this would be initiated every turn

    def __repr__(self):  # TODO: add VP
        return f"{self.name}: {self.hand}, {self.draw_pile}, {self.discard_pile}"

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

    def estimate_victory_points(self, game) -> int:  # TODO: make property
        """
        Calculate the victory points by Player's cards and other places.

        Returns:
            Sum of victory points.
        """
        vp = self.achieved_victory_points
        for card in self._all_cards:
            vp += card.estimate_vp_worth(game)
        return vp

    def on_turn_start(self, my_turn: bool):  # TODO: move to effects
        self.init_turn_state(my_turn)
        if my_turn:
            self.turns_played += 1

    def init_turn_state(self, my_turn: bool):
        """
        Initiate the state of current turn.
        By Default:
            * On my turns - is initiated with 1 action, 1 buy and 0 coins.
            * On my turns - is initiated with 0 action, 0 buy and 0 coins.

        Args:
            my turn: is current turn mine.
        """
        if my_turn:
            self.turn_stats = PlayerTurnStats(actions=1, buys=1, coins=0)
        else:
            self.turn_stats = PlayerTurnStats(actions=0, buys=0, coins=0)

    def detailed_repr(self, game):
        return f"{self.name}[{self.estimate_victory_points(game)} VP]: " \
               f"{self.hand.detailed_repr()}{self.draw_pile.detailed_repr()}" \
               f"{self.discard_pile.detailed_repr()}"

    def get_cards_alphabetically(self) -> list[BaseCard]:
        return sorted(self._all_cards, key=lambda x: x.name)

    def get_cards_by_value(self) -> list[BaseCard]:
        return sorted(self._all_cards, key=lambda x: x.value)

    def gain_cards(self, cards: BaseCard | list[BaseCard]):
        cards = (cards,) if type(cards) is BaseCard else cards
        for card in cards:
            self._all_cards.append(card)

    def remove_cards(self, cards: BaseCard | list[BaseCard]):
        cards = (cards,) if type(cards) is BaseCard else cards
        for card in cards:
            self._all_cards.remove(card)
