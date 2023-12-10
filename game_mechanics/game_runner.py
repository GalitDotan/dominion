from threading import Thread

from game_mechanics.game import Game


class GameRunner:
    """
    Runs a game of Dominion.
    """

    @classmethod
    def _run(cls, game: Game):
        """
        This function runs the given game from beginning to end.
        """
        game.run()

    @classmethod
    def threaded_run(cls, game: Game) -> Thread:
        """
        Runs a Dominion in a new Thread.

        Params:
            game: The game to run.

        Returns:
             The running thread
        """
        th = Thread(target=GameRunner._run, args=(game,))
        th.run()
        return th
