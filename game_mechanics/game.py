from random import shuffle
from typing import Optional

from game_mechanics.card_structures.supply_pile import SupplyPile
from game_mechanics.card_structures.trash import Trash
from game_mechanics.player.bot_player import BotPlayer
from game_mechanics.player.human_player import HumanPlayer
from game_mechanics.player.player import Player
from game_mechanics.screens.openning_message import OpeningMessage
from game_mechanics.screens.score_board import ScoreBoard
from game_mechanics.supply import Supply
from game_mechanics.turn.turn import Turn
from game_supplies.card_types.card import Card
from game_supplies.card_types.curse import Curse
from game_supplies.cards.dominion.kingdom_cards.cellar import Cellar
from game_supplies.cards.dominion.kingdom_cards.market import Market
from game_supplies.cards.dominion.kingdom_cards.merchant import Merchant
from game_supplies.cards.dominion.kingdom_cards.militia import Militia
from game_supplies.cards.dominion.kingdom_cards.mine import Mine
from game_supplies.cards.dominion.kingdom_cards.moat import Moat
from game_supplies.cards.dominion.kingdom_cards.remodel import Remodel
from game_supplies.cards.dominion.kingdom_cards.smithy import Smithy
from game_supplies.cards.dominion.kingdom_cards.village import Village
from game_supplies.cards.dominion.kingdom_cards.workshop import Workshop
from game_supplies.cards.dominion.standard_cards.Copper import Copper
from game_supplies.cards.dominion.standard_cards.Duchy import Duchy
from game_supplies.cards.dominion.standard_cards.Estate import Estate
from game_supplies.cards.dominion.standard_cards.Gold import Gold
from game_supplies.cards.dominion.standard_cards.Province import Province
from game_supplies.cards.dominion.standard_cards.Silver import Silver


def get_default_player_cards() -> list[Card]:
    """
    Get default cards: 7 Coppers and 3 Estates.
    """
    coppers: list[Card] = [Copper() for _ in range(7)]
    estates: list[Card] = [Estate() for _ in range(3)]
    return coppers + estates


def _generate_supply_piles(supply_card_types: tuple, supply_pile_sizes: Optional[tuple[int, ...]] = None) -> list[
    SupplyPile]:  # TODO: change input to list[tuple(Card, int]]
    """
    Receives a list of card types and the size of each pile.
    :return: A list of supply piles.
    """
    supply_pile_sizes = supply_pile_sizes if supply_pile_sizes else [Game._DEFAULT_PILE_SIZE for _ in
                                                                     range(len(supply_card_types))]
    return [SupplyPile(cards=[card_type() for _ in range(pile_size)]) for card_type, pile_size in
            zip(supply_card_types, supply_pile_sizes)]


class Game:
    _FIRST_GAME_CARDS = (Cellar, Moat, Merchant, Village, Workshop, Militia, Remodel, Smithy, Market, Mine)
    _STANDARD_CARDS = (Province, Duchy, Estate, Curse, Gold, Silver, Copper)
    _MIN_PLAYERS = 2
    _MAX_PLAYERS = 6
    _DEFAULT_PILE_SIZE = 10
    _DEFAULT_PLAYERS_NUM = 2
    _DEFAULT_HUMAN_NAME = "Siri"

    _V_CARDS_PER_PLAYERS = {
        2: 8,
        3: 12,
        4: 12,
        5: 15,
        6: 15
    }

    _CURSES_CARDS_PER_PLAYER = {
        2: 10,
        3: 20,
        4: 30,
        5: 40,
        6: 50
    }

    _DEFAULT_FINISH_PILES = (Province().name,)

    _EMPTY_PILES_FOR_FINISH_BY_NUM_PLAYERS = {
        2: 3,
        3: 3,
        4: 3,
        5: 4,
        6: 4
    }

    _MAX_EMPTY_PILES = 3

    def __init__(self, num_players: int = _DEFAULT_PLAYERS_NUM,
                 start_cards: list[Card] = None):
        """
        Initiate a single-player Dominion game.

        :param num_players: Number of _players_order, including the real player.
        :param start_cards: Which cards each player receives at the beginning of the game.
        """
        self._num_players = num_players
        self._start_cards = start_cards if start_cards else get_default_player_cards()

        self._validate_num_players()

        self._my_player = HumanPlayer(self._start_cards, name=Game._DEFAULT_HUMAN_NAME)
        self._bot_players = [BotPlayer(self._start_cards) for _ in range(self._num_players - 1)]

        self._players_order: list[Player] = self._bot_players.copy()
        self._players_order.append(self._my_player)
        shuffle(self._players_order)

        self.player_index = 0

        num_v_cards = Game._V_CARDS_PER_PLAYERS[self._num_players]
        num_curses = Game._CURSES_CARDS_PER_PLAYER[self._num_players]
        sizes = (num_v_cards, num_v_cards, num_v_cards, num_curses, 30, 40, 60)

        kingdom_piles = _generate_supply_piles(Game._FIRST_GAME_CARDS)
        standard_piles = _generate_supply_piles(Game._STANDARD_CARDS, sizes)
        self._supply = Supply(kingdom_piles, standard_piles)

        self._trash = Trash(name="Trash")

    def _validate_num_players(self):
        """
        Check that the number of _players_order is valid.

        :raise: ValueError
        """
        if self._num_players < Game._MIN_PLAYERS or self._num_players > Game._MAX_PLAYERS:
            raise ValueError("Number of _players_order has to be between 2 and 6")

    def to_next_player(self):
        """
        Update next player index.
        """
        self.player_index = (self.player_index + 1) % self._num_players

    def run(self):
        """
        Run a single-player Dominion game.
        """
        print(OpeningMessage(self._my_player, self._bot_players))

        while not self._game_over():
            curr_player = self._players_order[self.player_index]
            other_players = self._players_order.copy()
            other_players.remove(curr_player)

            turn = Turn(curr_player, other_players, self._supply, self._trash)
            turn.play()
            self.to_next_player()

        score_bard = ScoreBoard(self._players_order)
        print(score_bard)

    def _is_enough_empty_piles(self) -> bool:
        return self._supply.get_num_of_empty() >= Game._EMPTY_PILES_FOR_FINISH_BY_NUM_PLAYERS[self._num_players]

    def _is_any_of_finishing_piles_empty(self, finishing_piles: tuple[str]) -> bool:
        empty_pile_names = [pile.name for pile in self._supply.empty_piles]
        for pile in finishing_piles:
            if pile in empty_pile_names:
                return True
        return False

    def _game_over(self, finishing_piles: tuple[str] = _DEFAULT_FINISH_PILES) -> bool:
        """
        Check whether any of the end conditions are met.
        """
        return self._is_enough_empty_piles() or self._is_any_of_finishing_piles_empty(finishing_piles)
