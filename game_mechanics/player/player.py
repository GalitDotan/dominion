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
    A Dominion curr_player.
    """

    def __init__(self, cards: list[Card], name: Optional[str] = None):
        self.name = name if name else generate_name()
        self.turns_played = 0
        self.state = PlayerState(cards=cards)
        self.turn_state: Optional[PlayerTurnState] = None  # this would be initiated every turn

    def __repr__(self):
        return f"{self.name}{self.state}"

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
        return self.state.victory_points

    def on_game_start(self):
        pass

    def on_turn_start(self, my_turn: bool):
        self.init_turn_state(my_turn)
        if my_turn:
            self.turns_played += 1

    def get_board_view(self) -> str:
        pass  # TODO: board view by curr_player

    def detailed_repr(self):
        return f"{self.name}{self.state.detailed_repr()}"

    def init_turn_state(self, my_turn: bool):
        """
        Initiate the state of current turn.
        By Default:
            * On my turns - is initiated with 1 action, 1 buy and 0 coins.
            * On my turns - is initiated with 0 action, 0 buy and 0 coins.

        Params:
            my turn: is current turn mine.
        """
        if my_turn:
            self.turn_state = PlayerTurnState(actions=1, buys=1, coins=0)
        else:
            self.turn_state = PlayerTurnState(actions=0, buys=0, coins=0)

    def play_card_from_hand(self, card: Card, turn_state: PlayerTurnState):
        """
        Play a card from _play_order hand and update state accordingly.

        :param card: the card.
        :param turn_state: current game_stages state.
        """
        if card not in self.state.hand:
            raise ValueError(f"{card} is not in {self.state.hand}")

        self.state.hand.remove(card)
        self.state.play_area.play(card)

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
        if self.state.draw_pile.is_empty():
            self.shuffle_discard_to_draw_pile()
        return self.state.draw_pile.draw()

    def draw_cards(self, amount: int):
        """
        Draw a card `amount` times.
        If the Draw and DiscardCard piles got emptied - it could return less than the desired `amount` of cards.
        """
        cards = [self.draw_card() for _ in range(amount)]
        return [card for card in cards if card]  # card could be None

    def draw_hand(self, num: int = 5):
        return self.draw_cards(num)

    def discard_hand(self):
        """
        Move all cards from hand to DiscardCard pile.
        """
        cards = self.state.hand.remove_all()
        self.state.discard_pile.put_all(cards)

    def discard_play(self):
        """
        Move all non-Duration cards from the Play Area to the DiscardCard pile.
        """
        cards = self.state.play_area.do_cleanup()
        self.state.discard_pile.put_all(cards)

    def shuffle_discard_to_draw_pile(self):
        """
        Shuffle all cards in the DiscardCard pile and put them on the bottom of the Draw pile.
        """
        cards = self.state.discard_pile.draw_all()
        shuffle(cards)
        self.state.discard_pile.put_all(cards)
