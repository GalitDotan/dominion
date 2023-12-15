from random import shuffle
from typing import Optional

from game_mechanics.card_structures.trash import Trash
from game_mechanics.game_config.game_config import GameConfiguration
from game_mechanics.states.player_state import PlayerState
from game_mechanics.supply import Supply


class GameState:
    """
    All changeable elements of the game would be here.
    """

    def __init__(self, game_conf: GameConfiguration):
        """
        Establish curr_player order.
        Initiate all the card structures that are part of the game.

        Params:
            game_conf: a "ready" dominion configuration.
        """
        self.game_conf = game_conf

        self.supply = Supply(
            kingdom_piles=self.game_conf.generate_supply_piles(self.game_conf.kingdom_piles_generators),
            standard_piles=self.game_conf.generate_supply_piles(self.game_conf.standard_piles_generators))
        self.trash = Trash(name="Trash")

        self.players: dict[str, PlayerState] = {player_name: PlayerState(cards=[], name=player_name) for player_name in
                                                self.game_conf.player_names}

        self._play_order: list[str] = list(self.players.keys())
        shuffle(self._play_order)

        self.player_index = 0
        self._num_players = len(self.players)

    def __hash__(self):
        return hash(self.game_conf)

    def run_game(self):
        pass

    @property
    def curr_player(self):
        return self._play_order[self.player_index]

    @property
    def player_list(self):
        return list(self.players.values())

    def get_player_opponents(self, player: Optional[str] = None) -> list[str]:
        """
        Get all the opponents of a curr_player.
        If no curr_player name was supplied - returns the opponents of the current curr_player.

        Params:
            player_name: the curr_player's name

        Returns:
            A list of opponents (players).
        """
        if not player:
            player = self.curr_player
        opponents = self.get_player_opponents(player)
        opponents.remove(player)
        return list(opponents)

    def move_to_next_player(self):
        """
        Update next curr_player index.
        """
        self.player_index = (self.player_index + 1) % self._num_players

    def start(self):
        """
        Generate the initial game state.
        """
        num_v_cards = V_CARDS_PER_PLAYERS[self._num_players]
        num_curses = CURSES_CARDS_PER_PLAYER[self._num_players]
        sizes = (num_v_cards, num_v_cards, num_v_cards, num_curses, 30, 40, 60)
        kingdom_piles = generate_supply_piles(FIRST_GAME_CARDS)  # TODO: allow other cards
        standard_piles = generate_supply_piles(STANDARD_CARDS, sizes)
        self.game_state = GameState(kingdom_piles, standard_piles, self.players)

    def run(self):
        """
        Run this game.
        """
        self.status = GameStatus.IN_PROGRESS
        while self.status == GameStatus.IN_PROGRESS:
            curr_player = self.game_state.curr_player
            opponents = self.game_state.get_player_opponents()

            turn = Turn(curr_player, opponents, self.game_state)
            turn.play()
            self.game_state.move_to_next_player()

    def get_player_view(self, player_name: str):
        """
        Get current board view from the PoV of the given curr_player.
        """
        player = self.players[player_name]
        opponents = self.game_state.get_player_opponents(player)
        if self.status == GameStatus.INITIATED:
            return OpeningMessage(player, opponents)
        elif self.status == GameStatus.IN_PROGRESS:
            return player.get_board_view()
        elif self.status == GameStatus.FINISHED:
            return ScoreBoard(self.player_list)
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
