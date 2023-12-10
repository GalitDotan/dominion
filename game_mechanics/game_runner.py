from threading import Thread

from game_mechanics.game_master import GameMaster


class GameRunner:
    """
    Runs a game of Dominion.
    """

    @classmethod
    def _run(cls, gm: GameMaster):
        """
        This function runs the given game from beginning to end.
        """
        gm.run_game()

    @classmethod
    def threaded_run(cls, gm: GameMaster) -> Thread:
        """
        Runs a Dominion in a new Thread.

        Params:
            game: The game to run.

        Returns:
             The running thread
        """
        th = Thread(target=GameRunner._run, args=(gm,))
        th.run()
        return th
