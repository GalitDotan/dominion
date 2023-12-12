from threading import Thread

from game_mechanics.states.game_state import GameState


class GameRunner:
    """
    Runs a game of Dominion.
    """

    @classmethod
    def _run(cls, gm: GameState):
        """
        This function runs the given game from beginning to end.
        """
        gm.run_game()

    @classmethod
    def threaded_run(cls, gm: GameState) -> Thread:
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
