from random import shuffle
from typing import Optional

from game_mechanics.card_structures.trash import Trash
from game_mechanics.effects.effect import Effect
from game_mechanics.effects.game_setup import GameSetup
from game_mechanics.effects.game_stages.phase.end_game_phase import EndGamePhase
from game_mechanics.game_config.game_conf_consts import EMPTY_PILES_FOR_FINISH_BY_NUM_PLAYERS
from game_mechanics.game_config.game_config import GameConfiguration
from game_mechanics.game_status import GameStatus
from game_mechanics.game_supplies.cards_packs.all_cards import Card
from game_mechanics.states.player_state import Player
from game_mechanics.supply import Supply


class PlayerTurn(Effect):
    def activate(self, game):
        curr_player = game.curr_player
        opponents = game.get_player_opponents()


class Game:
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

        self.players: dict[str, Player] = {player_name: Player(cards=[], name=player_name) for player_name in
                                           self.game_conf.player_names}

        self._play_order: list[str] = list(self.players.keys())
        shuffle(self._play_order)

        self.player_index = 0
        self._num_players = len(self.players)

        self.applied_effects: list[Effect] = []

    def __hash__(self):
        return hash(self.game_conf)

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

    def is_in_progress(self) -> bool:
        return self.game_conf.status == GameStatus.IN_PROGRESS

    def run(self):
        """
        Run this game.
        """
        self.game_conf.status = GameStatus.IN_PROGRESS
        self.apply_effect(GameSetup())
        while not self.game_over():
            self.apply_effect(PlayerTurn())
        self.apply_effect(EndGamePhase())

    def apply_effect(self, effect: Effect):
        """
        Activate given effect and add it to the list.
        """
        effect.activate(self)
        self.applied_effects.append(effect)

    def game_over(self, finishing_piles: tuple[str] = (Card.PROVINCE,)) -> bool:
        """
        Check whether any of the end conditions are met.
        """
        return self._is_enough_empty_piles() or self._is_any_of_finishing_piles_empty(finishing_piles)

    def _is_enough_empty_piles(self) -> bool:
        return self.supply.get_num_of_empty() >= EMPTY_PILES_FOR_FINISH_BY_NUM_PLAYERS[self._num_players]

    def _is_any_of_finishing_piles_empty(self, finishing_piles: tuple[str]) -> bool:
        empty_pile_names = [pile.name for pile in self.supply.empty_piles]
        for pile in finishing_piles:
            if pile in empty_pile_names:
                return True
        return False
