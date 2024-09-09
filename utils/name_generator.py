import random

from wonderwords import RandomWord

RW = RandomWord()

available_names = [
    'SIRI',  # Apple's voice assistant (and my username in the OG dominion game)
    'GALA',  # my nickname :)
    'LIBI',  # no reference
    'KIKI',  # 'Baba is You' game
    'BABA',  # 'Baba is You' game
    'NIMI',  # no reference
    'LILY',  # different characters
    'ZAZA',  # no reference
    'MOJO',  # 'The Powerpuff Girls'
    'JOJO',  # 'The Powerpuff Girls'
    'MIMI',  # no reference
    'NANA',  # no reference
    'ROBO',  # generic robot name
    'LUCA',  # Disney's 'Luca'
    'GAGA',  # famous singer
    'LOLO',  # no reference
    'MOKO',  # no reference
    'DIDI',  # no reference
    'TOTO',  # 'The Wizard of Oz'
    'ZAZI',  # no reference
    'DORA',  # 'Dora the Explorer'
    'LILO',  # 'Lilo & Stitch'
    'RICKI',  # different characters
    'BIMO',  # Adventure Time
    'TINA',  # different characters
    'MOMO',  # 'Avatar: The Last Airbender'
    'ZAZU',  # 'The Lion King'
]

GAME_NAME_FORMAT = "{host_name}'s {adj} Game"


def generate_player_name() -> str:
    """
    Generate a player's name.
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
