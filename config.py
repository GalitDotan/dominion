class Endpoints:
    INIT_GAME = '/init-game'
    START_GAME = '/start-game'
    JOIN_GAME = '/join-game'
    VIEW_GAME_BOARD = '/view-game-board'
    GAME_STATUS = '/game-status'
    GET_DECISION = '/get-decision'
    DECIDE = '/decide'
    VIEW_PLAYERS = '/view-players'
    ADD_BOT = '/add-bot-to-game'  # TODO: implement this


class ServerConf:
    HOST: str = '0.0.0.0'
    PORT = 8000
    SCHEMA = 'ws'
    IP = 'localhost'


class HeadlineFormats:
    H1 = "                   ***  {}  ***                   "
    H2 = "  ###  {}  ###"
    H3 = "      ##  {}"
    H4 = "          *  {}"
