from game_mechanics.game_supplies.cards_packs.dominion.standard_cards.Province import Province

MIN_PLAYERS = 2
MAX_PLAYERS = 6
DEFAULT_PILE_SIZE = 10
DEFAULT_PLAYERS_NUM = 2

DEFAULT_FINISH_PILES = (Province().name,)

EMPTY_PILES_FOR_FINISH_BY_NUM_PLAYERS = {
    2: 3,
    3: 3,
    4: 3,
    5: 4,
    6: 4
}

MAX_EMPTY_PILES = 3
