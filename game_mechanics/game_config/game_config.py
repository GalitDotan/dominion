from typing import Optional, Callable, Any
from uuid import uuid4

from pydantic import BaseModel
from pydantic import Field
from pydantic.functional_validators import model_validator

from game_mechanics.card_structures.supply_pile import SupplyPile
from game_mechanics.game_config.game_conf_consts import DEFAULT_PILE_SIZE, DEFAULT_COPPER_AMOUNT, \
    DEFAULT_SILVER_AMOUNT, DEFAULT_GOLD_AMOUNT, V_CARDS_PER_PLAYERS, CURSES_CARDS_PER_PLAYER
from game_mechanics.game_status import GameStatus
from game_mechanics.game_supplies.all_cards import Card


def victory_cards_by_players(game_conf: 'GameConfiguration') -> int:
    return V_CARDS_PER_PLAYERS[game_conf.num_players]


def curse_cards_by_players(game_conf: 'GameConfiguration') -> int:
    return CURSES_CARDS_PER_PLAYER[game_conf.num_players]


class PileGenerator(BaseModel):
    generators: Card | tuple[Card, Optional[Callable[['GameConfiguration'], int] | int]] | list[
        tuple[Card, Optional[Callable[['GameConfiguration'], int] | int]]]
    name: Card

    @model_validator(mode='before')
    @classmethod
    def validate_name(cls, data: Any):
        if 'name' not in data:
            generators = data['generators']
            if type(generators) is Card:
                name = generators
            elif type(generators) is tuple:
                name = generators[0]
            else:  # if there is more than one type of card in the pile
                name = data['generators'][-1][0]  # the name of the top card
            data['name'] = name
        return data


class GameConfiguration(BaseModel):
    """
    The configuration of the game:
    Which cards does the game include,
    The players.
    """

    class Config:
        arbitrary_types_allowed = True

    game_id: str = Field(default_factory=lambda: str(uuid4()))
    player_names: list[str] = []
    status: GameStatus = GameStatus.INITIATED
    kingdom_piles_generators: list[PileGenerator] = [
        PileGenerator(generators=Card.CELLAR),
        PileGenerator(generators=Card.MOAT),
        PileGenerator(generators=Card.MERCHANT),
        PileGenerator(generators=Card.VILLAGE),
        PileGenerator(generators=Card.WORKSHOP),
        PileGenerator(generators=Card.MILITIA),
        PileGenerator(generators=Card.REMODEL),
        PileGenerator(generators=Card.SMITHY),
        PileGenerator(generators=Card.MARKET),
        PileGenerator(generators=Card.MINE),
    ]
    standard_piles_generators: list[PileGenerator] = [
        PileGenerator(generators=(Card.PROVINCE, victory_cards_by_players)),
        PileGenerator(generators=(Card.DUCHY, victory_cards_by_players)),
        PileGenerator(generators=(Card.ESTATE, victory_cards_by_players)),
        PileGenerator(generators=(Card.GOLD, DEFAULT_GOLD_AMOUNT)),
        PileGenerator(generators=(Card.SILVER, DEFAULT_SILVER_AMOUNT)),
        PileGenerator(generators=(Card.COPPER, DEFAULT_COPPER_AMOUNT)),
        PileGenerator(generators=(Card.CURSE, curse_cards_by_players)),
    ]

    def __hash__(self):
        return hash(self.game_id)

    def __repr__(self):
        return f'{self.game_id}[{self.status}]:{self.player_names}'

    @property
    def num_players(self):
        return len(self.player_names)

    def generate_supply_piles(self, pile_generators: list[PileGenerator]) -> list[SupplyPile]:
        """
        Get a list of Supply Piles from a list of pile generators.

        Params:
            pile_generators: The generators.

        Returns:
            A list of Supply Piles.
        """
        return [self._generate_pile(generator) for generator in pile_generators]

    def _generate_pile(self, pile_generator: PileGenerator) -> SupplyPile:
        """
        Generate a supply pile by this configuration.

        Returns:
            The pile.
        """
        cards = []
        if type(pile_generator.generators) is Card:
            card: Card = pile_generator.generators
            cards = [card.value() for _ in range(DEFAULT_PILE_SIZE)]
        elif type(pile_generator.generators) is tuple:
            card, amount_generator = self.generators
            cards = [card.value() for _ in range(amount_generator(self))]
        else:  # if there is more than one type of card in the pile
            for card_name, pile_generator in self.generators:
                if pile_generator is None:
                    num_cards = DEFAULT_PILE_SIZE
                elif type(pile_generator) is int:
                    num_cards = pile_generator
                else:
                    pile_generator: Callable[[GameConfiguration], int]
                    num_cards = pile_generator(self.game_conf)
                cards.extend([card_name.value() for _ in range(num_cards)])
        return SupplyPile(cards)
