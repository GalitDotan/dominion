from typing import Optional, Callable, Any

from pydantic import BaseModel
from pydantic.functional_validators import model_validator

from game_mechanics.game_config.game_config import GameConfiguration
from game_mechanics.game_supplies.cards_packs.all_cards import Card


class PileGenerator(BaseModel):
    generators: Card | tuple[Card, Optional[Callable[[GameConfiguration], int] | int]] | list[
        tuple[Card, Optional[Callable[[GameConfiguration], int] | int]]]
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
