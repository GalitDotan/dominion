from typing import Optional, Callable, Any

from pydantic import BaseModel
from pydantic.functional_validators import model_validator

from app_utils.connection_manager import WebSocketsManager
from game_mechanics.card_structures.supply_pile import SupplyPile
from game_mechanics.game_config.game_conf_consts import DEFAULT_PILE_SIZE, DEFAULT_COPPER_AMOUNT, \
    DEFAULT_SILVER_AMOUNT, DEFAULT_GOLD_AMOUNT, V_CARDS_PER_PLAYERS, CURSES_CARDS_PER_PLAYER, ESTATES_AMOUNT_SETUP
from game_mechanics.game_status import GameStatus
from game_mechanics.game_supplies.all_cards import CardInitiator, Expansion
from utils.name_generator import generate_game_name


def victory_cards_by_players(game_conf: 'GameConfiguration') -> int:
    return V_CARDS_PER_PLAYERS[game_conf.num_players]


def estate_cards_by_players(game_conf: 'GameConfiguration') -> int:
    in_supply = V_CARDS_PER_PLAYERS[game_conf.num_players]
    return in_supply + (ESTATES_AMOUNT_SETUP * game_conf.num_players)


def curse_cards_by_players(game_conf: 'GameConfiguration') -> int:
    return CURSES_CARDS_PER_PLAYER[game_conf.num_players]


class PileInitiator(BaseModel):
    """
    Generator for supply piles_sorted.
    """
    initiators: CardInitiator | tuple[CardInitiator, Optional[Callable[['GameConfiguration'], int] | int]] | list[
        tuple[CardInitiator, Optional[Callable[['GameConfiguration'], int] | int]]]
    name: str

    @model_validator(mode='before')
    @classmethod
    def validate_name(cls, data: Any):
        if 'name' not in data:
            initiators = data['initiators']
            if type(initiators) is CardInitiator:
                card_initiator = initiators
            elif type(initiators) is tuple:
                card_initiator = initiators[0]
            else:  # if there is more than one type of card in the pile
                card_initiator = data['initiators'][-1][0]  # the name of the top card
            data['name'] = card_initiator.name
        return data


class GameConfiguration(BaseModel):
    """
    The configuration of the game:
    Which cards does the game include,
    The players.
    """

    class Config:
        arbitrary_types_allowed = True

    host_player_name: str
    game_name: str
    player_names: list[str] = []
    status: GameStatus = GameStatus.INITIATED
    expansions: Expansion = Expansion.BASE
    kingdom_piles_initiators: list[PileInitiator] = [
        PileInitiator(initiators=CardInitiator.CELLAR),
        PileInitiator(initiators=CardInitiator.MOAT),
        PileInitiator(initiators=CardInitiator.MERCHANT),
        PileInitiator(initiators=CardInitiator.VILLAGE),
        PileInitiator(initiators=CardInitiator.WORKSHOP),
        PileInitiator(initiators=CardInitiator.MILITIA),
        PileInitiator(initiators=CardInitiator.REMODEL),
        PileInitiator(initiators=CardInitiator.SMITHY),
        PileInitiator(initiators=CardInitiator.MARKET),
        PileInitiator(initiators=CardInitiator.MINE),
    ]
    standard_piles_initiators: list[PileInitiator] = [
        PileInitiator(initiators=(CardInitiator.PROVINCE, victory_cards_by_players)),
        PileInitiator(initiators=(CardInitiator.DUCHY, victory_cards_by_players)),
        PileInitiator(initiators=(CardInitiator.ESTATE, estate_cards_by_players)),
        PileInitiator(initiators=(CardInitiator.GOLD, DEFAULT_GOLD_AMOUNT)),
        PileInitiator(initiators=(CardInitiator.SILVER, DEFAULT_SILVER_AMOUNT)),
        PileInitiator(initiators=(CardInitiator.COPPER, DEFAULT_COPPER_AMOUNT)),
        PileInitiator(initiators=(CardInitiator.CURSE, curse_cards_by_players)),
    ]
    ws_manager: WebSocketsManager

    @model_validator(mode='before')
    @classmethod
    def validate_names(cls, data: Any):
        if 'host_player_name' not in data:
            data['host_player_name'] = data['player_names'][0]
        if 'game_name' not in data:
            host_player_name = data['host_player_name']
            data['game_name'] = generate_game_name(host_player_name)
        return data

    def __hash__(self):
        return hash(self.game_name)

    def __repr__(self):
        return f'~ {self.game_name} ~ Players: {self.player_names}'

    @property
    def num_players(self):
        return len(self.player_names)

    def generate_supply_piles(self, pile_initiators: list[PileInitiator]) -> list[SupplyPile]:
        """
        Get a list of Supply Piles from a list of pile initiators.

        Args:
            pile_initiators: The initiators.

        Returns:
            A list of Supply Piles.
        """
        return [self._generate_pile(generator) for generator in pile_initiators]

    def _generate_pile(self, pile_generator: PileInitiator) -> SupplyPile:
        """
        Generate a supply pile by this configuration.

        Returns:
            The pile.
        """
        cards = []
        if type(pile_generator.initiators) is CardInitiator:
            card: CardInitiator = pile_generator.initiators
            cards = [card.value() for _ in range(DEFAULT_PILE_SIZE)]
        elif type(pile_generator.initiators) is tuple:
            card, amount_calculator = pile_generator.initiators
            if type(amount_calculator) is int:
                cards = [card.value() for _ in range(amount_calculator)]
            else:
                cards = [card.value() for _ in range(amount_calculator(self))]
        else:  # if there is more than one type of card in the pile
            for card_name, pile_generator in pile_generator.initiators:
                if pile_generator is None:
                    num_cards = DEFAULT_PILE_SIZE
                elif type(pile_generator) is int:
                    num_cards = pile_generator
                else:
                    pile_generator: Callable[[GameConfiguration], int]
                    num_cards = pile_generator(self)
                cards.extend([card_name.value() for _ in range(num_cards)])
        return SupplyPile(cards)
