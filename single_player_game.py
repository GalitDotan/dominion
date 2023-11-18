from random import shuffle
from typing import List, Tuple

from game_mechanics.card_structures.trash import Trash
from game_mechanics.end_conditions import game_over
from game_mechanics.card_structures.pile import Pile
from game_mechanics.player.player import Player
from game_mechanics.supply import Supply
from game_supplies.card_types.card import Card, Curse
from game_supplies.cards.base.basic_supply_cards.Copper import Copper
from game_supplies.cards.base.basic_supply_cards.Duchy import Duchy
from game_supplies.cards.base.basic_supply_cards.Estate import Estate
from game_supplies.cards.base.basic_supply_cards.Gold import Gold
from game_supplies.cards.base.basic_supply_cards.Province import Province
from game_supplies.cards.base.basic_supply_cards.Silver import Silver
from game_supplies.cards.base.kingdom_cards.cellar import Cellar
from game_supplies.cards.base.kingdom_cards.market import Market
from game_supplies.cards.base.kingdom_cards.merchant import Merchant
from game_supplies.cards.base.kingdom_cards.militia import Militia
from game_supplies.cards.base.kingdom_cards.mine import Mine
from game_supplies.cards.base.kingdom_cards.moat import Moat
from game_supplies.cards.base.kingdom_cards.remodel import Remodel
from game_supplies.cards.base.kingdom_cards.smithy import Smithy
from game_supplies.cards.base.kingdom_cards.village import Village
from game_supplies.cards.base.kingdom_cards.workshop import Workshop

FIRST_GAME_CARDS = (Cellar, Moat, Merchant, Village, Workshop, Militia, Remodel, Smithy, Market, Mine)
OTHER_CARDS = (Province, Duchy, Estate, Curse, Gold, Silver, Copper)


def _get_default_player_cards() -> List[Card]:
    coppers: List[Card] = [Copper() for _ in range(7)]
    estates: List[Card] = [Estate() for _ in range(3)]
    return coppers + estates


def _generate_piles(card_types: Tuple, pile_size: int = 10) -> List[Pile]:
    return [Pile(cards=[card_type() for _ in range(pile_size)], ) for card_type in card_types]


def run(num_players: int = 2, start_cards: List[Card] = None):
    if num_players < 2 or num_players > 6:
        raise ValueError("Number of players has to be between 2 and 6")

    start_cards = start_cards if start_cards else _get_default_player_cards()

    my_player = Player(start_cards)
    bot_players = [Player(start_cards) for _ in range(num_players)]

    players = bot_players.copy()
    players.append(my_player)
    shuffle(players)

    next_player_index = 0

    kingdom_piles = _generate_piles(card_types=FIRST_GAME_CARDS)
    other_piles = _generate_piles(card_types=OTHER_CARDS)
    supply = Supply(kingdom_piles, other_piles)

    trash = Trash()

    while not game_over(supply, num_players):
        curr_player = players[next_player_index]
        other_players = players.copy()
        other_players.remove(curr_player)

        play_turn(curr_player, other_players)

        next_player_index = (next_player_index + 1) % num_players


if __name__ == '__main__':
    run()
