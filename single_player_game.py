from random import shuffle

from game_mechanics.card_structures.supply_pile import SupplyPile
from game_mechanics.card_structures.trash import Trash
from game_mechanics.end_conditions import game_over
from game_mechanics.player.bot_player import BotPlayer
from game_mechanics.player.human_player import HumanPlayer
from game_mechanics.player.player import Player
from game_mechanics.supply import Supply
from game_mechanics.turn import Turn
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


def _get_default_player_cards() -> list[Card]:
    coppers: list[Card] = [Copper() for _ in range(7)]
    estates: list[Card] = [Estate() for _ in range(3)]
    return coppers + estates


def _generate_supply_piles(card_types: tuple, pile_size: int = 10) -> list[SupplyPile]:
    return [SupplyPile(cards=[card_type() for _ in range(pile_size)], ) for card_type in card_types]


def _display_score_board(players: list[Player]):
    players_by_score = sorted(players, reverse=True)
    print(f"*** The winner is {players_by_score[0]} ***")
    for player in players:
        print(f"{player.name}: {player.victory_points} VP [{player.turns_played} turns]")


def _display_opening_message(my_player: Player, other_players: list[Player]):
    other_names = ', '.join([player.name for player in other_players])
    print(f"""
    ##############################################
        Welcome to Dominion, {my_player.name}!
        Meet your opponents: {other_names}
        Good Luck!
    ##############################################
    """)


def run(num_players: int = 2, start_cards: list[Card] = None):
    if num_players < 2 or num_players > 6:
        raise ValueError("Number of players has to be between 2 and 6")

    start_cards = start_cards if start_cards else _get_default_player_cards()

    my_player = HumanPlayer(start_cards, name="Siri")
    bot_players = [BotPlayer(start_cards) for _ in range(num_players - 1)]

    players: list[Player] = bot_players.copy()
    players.append(my_player)
    shuffle(players)

    next_player_index = 0

    kingdom_piles = _generate_supply_piles(card_types=FIRST_GAME_CARDS)
    other_piles = _generate_supply_piles(card_types=OTHER_CARDS)
    supply = Supply(kingdom_piles, other_piles)

    trash = Trash(name="Trash")

    _display_opening_message(my_player, bot_players)

    while not game_over(supply, num_players):
        curr_player = players[next_player_index]
        other_players = players.copy()
        other_players.remove(curr_player)

        turn = Turn(curr_player, other_players, supply, trash)
        turn.play()

        next_player_index = (next_player_index + 1) % num_players

    _display_score_board(players)


if __name__ == '__main__':
    run()
