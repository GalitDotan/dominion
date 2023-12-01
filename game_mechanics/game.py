from random import shuffle
from typing import Optional

from consts import V_CARDS_PER_PLAYERS, CURSES_CARDS_PER_PLAYER, FIRST_GAME_CARDS, STANDARD_CARDS, DEFAULT_PILE_SIZE, \
    DEFAULT_FINISH_PILES, EMPTY_PILES_FOR_FINISH_BY_NUM_PLAYERS, GameStatus
from game_mechanics.card_structures.supply_pile import SupplyPile
from game_mechanics.game_stages.turn import Turn
from game_mechanics.game_supplies.card_types.card import Card
from game_mechanics.player.player import Player
from game_mechanics.screens.openning_message import OpeningMessage
from game_mechanics.screens.score_board import ScoreBoard
from game_mechanics.states.game_state import GameState


def _generate_supply_piles(supply_card_types: tuple, supply_pile_sizes: Optional[tuple[int, ...]] = None) -> list[
    SupplyPile]:  # TODO: change input to list[tuple(Card, int]]
    """
    Receives a list of card types and the size of each pile.
    :return: A list of supply piles.
    """
    supply_pile_sizes = supply_pile_sizes if supply_pile_sizes else [DEFAULT_PILE_SIZE for _ in
                                                                     range(len(supply_card_types))]
    return [SupplyPile(cards=[card_type() for _ in range(pile_size)]) for card_type, pile_size in
            zip(supply_card_types, supply_pile_sizes)]


class Game:
    def __init__(self, game_id: str, start_cards: list[Card], players: dict[str, Player]):
        """
        Initiate a single-player Dominion game.

        Params:
            game_id: the id of the game
            start_cards: a list of cards each player would receive at the beginning of the game.
            players: a list of players.
        """
        self.id = game_id
        self.status: GameStatus = GameStatus.INITIATED
        self._num_players = len(players)
        self._start_cards = start_cards

        self.players: dict[str, Player] = players
        self._play_order: list[Player] = list(self.players.values())
        shuffle(self._play_order)

        self.player_index = 0

        num_v_cards = V_CARDS_PER_PLAYERS[self._num_players]
        num_curses = CURSES_CARDS_PER_PLAYER[self._num_players]
        sizes = (num_v_cards, num_v_cards, num_v_cards, num_curses, 30, 40, 60)
        kingdom_piles = _generate_supply_piles(FIRST_GAME_CARDS)  # TODO: allow other cards
        standard_piles = _generate_supply_piles(STANDARD_CARDS, sizes)

        self.game_state: GameState = GameState(kingdom_piles, standard_piles)

    def __hash__(self):
        return self.id

    def __eq__(self, other):
        return self.id == other.id

    @property
    def curr_player(self):
        return self._play_order[self.player_index]

    def run(self):
        """
        Run this game.
        """
        self.status = GameStatus.IN_PROGRESS
        while self.status == GameStatus.IN_PROGRESS:
            curr_player = self.curr_player
            opponents = self.get_player_opponents()

            turn = Turn(curr_player, opponents, self.game_state)
            turn.play()
            self._to_next_player()

    def get_player_opponents(self, player: Optional[Player] = None) -> list[Player]:
        """
        Get all the opponents of a player.
        If no player name was supplied - returns the opponents of the current player.

        Params:
            player_name: the player's name

        Returns:
            A list of opponents (players).
        """
        if not player:
            player = self._play_order[self.player_index]
        opponents = self._play_order.copy()
        opponents.remove(player)
        return list(opponents)

    def get_player_view(self, player_name: str):
        """
        Get current board view from the PoV of the given player.
        """
        player = self.players[player_name]
        opponents = self.get_player_opponents(player)
        if self.status == GameStatus.INITIATED:
            return OpeningMessage(player, opponents)
        elif self.status == GameStatus.IN_PROGRESS:
            return player.get_board_view()
        elif self.status == GameStatus.FINISHED:
            return ScoreBoard(self._play_order)
        raise AttributeError(f'Unknown status {self.status}')

    def game_over(self, finishing_piles: tuple[str] = DEFAULT_FINISH_PILES) -> bool:
        """
        Check whether any of the end conditions are met.
        """
        return self._is_enough_empty_piles() or self._is_any_of_finishing_piles_empty(finishing_piles)

    def _is_enough_empty_piles(self) -> bool:
        return self.game_state.supply.get_num_of_empty() >= EMPTY_PILES_FOR_FINISH_BY_NUM_PLAYERS[self._num_players]

    def _is_any_of_finishing_piles_empty(self, finishing_piles: tuple[str]) -> bool:
        empty_pile_names = [pile.name for pile in self.game_state.supply.empty_piles]
        for pile in finishing_piles:
            if pile in empty_pile_names:
                return True
        return False

    def _to_next_player(self):
        """
        Update next player index.
        """
        self.player_index = (self.player_index + 1) % self._num_players
