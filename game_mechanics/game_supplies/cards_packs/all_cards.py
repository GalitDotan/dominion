from enum import Enum

from game_mechanics.game_supplies.cards_packs.dominion.kingdom_cards import *
from game_mechanics.game_supplies.cards_packs.dominion.standard_cards import *


class Card(Enum):
    # standard cards
    COPPER = Copper
    SILVER = Silver
    GOLD = Gold
    ESTATE = Estate
    DUCHY = Duchy
    PROVINCE = Province
    CURSE = Curse

    # base dominion
    CELLAR = Cellar
    MARKET = Market
    MERCHANT = Merchant
    MILITIA = Militia
    MINE = Mine
    MOAT = Moat
    REMODEL = Remodel
    SMITHY = Smithy
    VILLAGE = Village
    WORKSHOP = Workshop
