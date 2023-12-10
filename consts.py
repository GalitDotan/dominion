from enum import Enum


class GameStatus(Enum):
    INITIATED = 'INITIATED'
    IN_PROGRESS = 'IN_PROGRESS'
    FINISHED = 'FINISHED'


class HeadlineFormats:
    H1 = "                   ***  {}  ***                   "
    H2 = "  ###  {}  ###"
    H3 = "      ##  {}"
    H4 = "          *  {}"
