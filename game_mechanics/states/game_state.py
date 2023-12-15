from random import shuffle
from typing import Optional, Callable

from game_mechanics.card_structures.supply_pile.supply_pile import SupplyPile
from game_mechanics.card_structures.trash import Trash
from game_mechanics.effects.reactions.reaction import Reaction
from game_mechanics.game_config.game_config import GameConfiguration
from game_mechanics.game_options.game_options import GameOptions
from game_mechanics.game_supplies.cards_packs.all_cards import Card
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

        self.waiting_decisions: dict[str, Optional[GameOptions]] = {name: None for name in self._play_order}
        self.waiting_reactions: list[Reaction] = []

    def __hash__(self):
        return hash(self.game_conf)

    def run_game(self):
        pass

    @property
    def curr_player(self):
        return self._play_order[self.player_index]

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

    def get_decision(self, player_name: str):
        """
        Get the waiting decision of the given player name
        """
        return self.waiting_decisions[player_name]

    def apply_decision(self, player_name: str, option_chosen: list[int] | int):
        """
        Get the waiting decision of the given player name
        """
        decision: GameOptions = self.waiting_decisions[player_name]
        decision.decide(option_chosen)
        self.waiting_decisions[player_name] = None

    def _generate_supply_piles(self,
                               piles_requested: list[
                                   tuple[Card, Optional[Callable[[GameConfiguration], int] | int]]]):
        piles: list[SupplyPile] = []

        return piles
