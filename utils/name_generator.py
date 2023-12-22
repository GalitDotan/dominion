import random

from wonderwords import RandomWord

RW = RandomWord()

available_names = ['SIRI', 'LIBI', 'KIKI', 'BABA', 'NIMI', 'LILY']
GAME_NAME_FORMAT = "{host_name}'s {adj} Game"


def generate_player_name() -> str:
    """
    Generate a players name.
    """
    name = random.choice(available_names)
    available_names.remove(name)
    return name


def generate_game_name(host_name: str) -> str:
    """
    Generate a name for a game.
    """
    return GAME_NAME_FORMAT.format(host_name=host_name,
                                   adj=RW.word(include_parts_of_speech=['adjectives']))
