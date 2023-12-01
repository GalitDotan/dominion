from random import shuffle
from typing import Optional

from game_mechanics.card_structures.supply_pile import SupplyPile
from game_mechanics.card_structures.trash import Trash
from game_mechanics.player.player import Player
from game_mechanics.states.base_state import BasePublicState
from game_mechanics.supply import Supply


class GameState(BasePublicState):
    """
    The current state of the public elements of the game:
        1. The supply
        2. The trash
        3. Public mats
    """

    def __init__(self, kingdom_piles: list[SupplyPile], standard_piles: list[SupplyPile], players: dict[str, Player]):
        """
        Establish player order.
        Initiate all the card structures that are part of the game.

        Params:
            kingdom_piles: The kingdom piles.
            standard_piles: The other piles.
            players: All the players in the game.
        """
        self.supply = Supply(kingdom_piles, standard_piles)
        self.trash = Trash(name="Trash")

        self._play_order: list[Player] = list(players.values())
        shuffle(self._play_order)

        self.player_index = 0
        self._num_players = len(players)

    @property
    def curr_player(self):
        return self._play_order[self.player_index]

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
            player = self.curr_player
        opponents = self.get_player_opponents(player)
        opponents.remove(player)
        return list(opponents)

    def move_to_next_player(self):
        """
        Update next player index.
        """
        self.player_index = (self.player_index + 1) % self._num_players
