from game_mechanics.game_supplies.card_types.curse import Curse
from game_mechanics.game_supplies.cards_packs.dominion.kingdom_cards.cellar import Cellar
from game_mechanics.game_supplies.cards_packs.dominion.kingdom_cards.market import Market
from game_mechanics.game_supplies.cards_packs.dominion.kingdom_cards.merchant import Merchant
from game_mechanics.game_supplies.cards_packs.dominion.kingdom_cards.militia import Militia
from game_mechanics.game_supplies.cards_packs.dominion.kingdom_cards.mine import Mine
from game_mechanics.game_supplies.cards_packs.dominion.kingdom_cards.moat import Moat
from game_mechanics.game_supplies.cards_packs.dominion.kingdom_cards.remodel import Remodel
from game_mechanics.game_supplies.cards_packs.dominion.kingdom_cards.smithy import Smithy
from game_mechanics.game_supplies.cards_packs.dominion.kingdom_cards.village import Village
from game_mechanics.game_supplies.cards_packs.dominion.kingdom_cards.workshop import Workshop
from game_mechanics.game_supplies.cards_packs.dominion.standard_cards.Copper import Copper
from game_mechanics.game_supplies.cards_packs.dominion.standard_cards.Duchy import Duchy
from game_mechanics.game_supplies.cards_packs.dominion.standard_cards.Estate import Estate
from game_mechanics.game_supplies.cards_packs.dominion.standard_cards.Gold import Gold
from game_mechanics.game_supplies.cards_packs.dominion.standard_cards.Province import Province
from game_mechanics.game_supplies.cards_packs.dominion.standard_cards.Silver import Silver

FIRST_GAME_CARDS = (Cellar, Moat, Merchant, Village, Workshop, Militia, Remodel, Smithy, Market, Mine)
STANDARD_CARDS = (Province, Duchy, Estate, Curse, Gold, Silver, Copper)
MIN_PLAYERS = 2
MAX_PLAYERS = 6
DEFAULT_PILE_SIZE = 10
DEFAULT_PLAYERS_NUM = 2
V_CARDS_PER_PLAYERS = {
    2: 8,
    3: 12,
    4: 12,
    5: 15,
    6: 15
}
CURSES_CARDS_PER_PLAYER = {
    2: 10,
    3: 20,
    4: 30,
    5: 40,
    6: 50
}
DEFAULT_FINISH_PILES = (Province().name,)
EMPTY_PILES_FOR_FINISH_BY_NUM_PLAYERS = {
    2: 3,
    3: 3,
    4: 3,
    5: 4,
    6: 4
}
MAX_EMPTY_PILES = 3
