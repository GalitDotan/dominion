from random import shuffle
from typing import Optional

from game_mechanics.game_supplies.card_types.action_card import Action
from game_mechanics.game_supplies.card_types.attack_card import Attack
from game_mechanics.game_supplies.card_types.card import Card
from game_mechanics.game_supplies.card_types.night_card import Night
from game_mechanics.game_supplies.card_types.treasure_card import Treasure
from game_mechanics.states.player_state import PlayerState
from game_mechanics.states.player_turn_state import PlayerTurnState
from utils.name_generator import generate_name


class Player:
    """
    A Dominion player.
    """

    def __init__(self, cards: list[Card], name: Optional[str] = None):
        self.name = name if name else generate_name()
        self.turns_played = 0
        self.player_state = PlayerState(cards=cards)

    def __repr__(self):
        return f"{self.name}{self.player_state}"

    def __lt__(self, other: "Player"):  # is self losing to other
        return self.victory_points < other.victory_points or (
                self.victory_points == other.victory_points and self.turns_played >= other.turns_played)

    def __eq__(self, other: "Player"):
        return self.victory_points == other.victory_points

    def __gt__(self, other: "Player"):  # is self winning other
        return self.victory_points > other.victory_points or (
                self.victory_points == other.victory_points and self.turns_played < other.turns_played)

    @property
    def victory_points(self):
        return self.player_state.victory_points

    def on_game_start(self):
        pass

    def get_board_view(self) -> str:
        pass  # TODO: board view by player

    def detailed_repr(self):
        return f"{self.name}{self.player_state.detailed_repr()}"

    def play_card_from_hand(self, card: Card, turn_state: PlayerTurnState):
        """
        Play a card from _play_order hand and update state accordingly.

        :param card: the card.
        :param turn_state: current game_stages state.
        """
        if card not in self.player_state.hand:
            raise ValueError(f"{card} is not in {self.player_state.hand}")

        self.player_state.hand.remove(card)
        self.player_state.play_area.play(card)

        if isinstance(card, Treasure):
            turn_state.coins += card.coins
        if isinstance(card, Action):
            for cmd in card.commands:
                pass
        if isinstance(card, Attack):
            for cmd in card.attacks:
                pass
        if isinstance(card, Night):
            pass

    def draw_card(self):
        """
        Get a card from the Draw pile and put it in the Hand.
        """
        if self.player_state.draw_pile.is_empty():
            self.shuffle_discard_to_draw_pile()
        return self.player_state.draw_pile.draw()

    def draw_cards(self, amount: int):
        """
        Draw a card `amount` times.
        If the Draw and Discard piles got emptied - it could return less than the desired `amount` of cards.
        """
        cards = [self.draw_card() for _ in range(amount)]
        return [card for card in cards if card]  # card could be None

    def draw_hand(self, num: int = 5):
        return self.draw_cards(num)

    def discard_hand(self):
        """
        Move all cards from hand to Discard pile.
        """
        cards = self.player_state.hand.remove_all()
        self.player_state.discard_pile.put_all(cards)

    def discard_play(self):
        """
        Move all non-Duration cards from the Play Area to the Discard pile.
        """
        cards = self.player_state.play_area.do_cleanup()
        self.player_state.discard_pile.put_all(cards)

    def shuffle_discard_to_draw_pile(self):
        """
        Shuffle all cards in the Discard pile and put them on the bottom of the Draw pile.
        """
        cards = self.player_state.discard_pile.draw_all()
        shuffle(cards)
        self.player_state.discard_pile.put_all(cards)
