from pydantic import BaseModel

from game_mechanics.game_config.game_config import GameConfiguration


class GameConfigurations(BaseModel):
    _host_name_to_game_confs: dict[str, set[GameConfiguration]] = {}
    _game_conf_to_host_name: dict[GameConfiguration, str] = {}

    def __repr__(self):
        print('HERE!')
        return repr(self._host_name_to_game_confs)

    def __getitem__(self, host_name: str) -> set[GameConfiguration]:
        """
        Allows retrieving the set of GameConfiguration for a host_name with dictionary-like syntax, e.g., game_confs[host_name].
        """
        return self.get_confs(host_name)

    def __setitem__(self, host_name: str, game_conf: GameConfiguration):
        """
        Allows setting a GameConfiguration with dictionary-like syntax, e.g., game_confs[host_name] = game_conf.
        This calls the add_conf method.
        """
        if host_name not in self._host_name_to_game_confs:
            self._host_name_to_game_confs[host_name] = set()

        self._host_name_to_game_confs[host_name].add(game_conf)
        self._game_conf_to_host_name[game_conf] = host_name

    def empty(self) -> bool:
        return len(self._host_name_to_game_confs) == 0

    def get_host(self, game_conf: str | GameConfiguration) -> str:
        return self._game_conf_to_host_name[game_conf]

    def get_confs(self, host_name: str, game_name: str | None = None) -> set[GameConfiguration] | GameConfiguration:
        confs = self._host_name_to_game_confs[host_name]
        if not game_name:
            return confs
        if game_name not in confs:
            raise ValueError(f"Game {game_name} doesn't exist for host {host_name}")
        for game in confs:
            if hash(game) == game_name:
                return game

    def remove_conf(self, host_name: str, game_name: str) -> GameConfiguration:
        """
        Remove a specific GameConfiguration by host name and game name, and return the removed configuration.

        Args:
            host_name: The name of the host.
            game_name: The name of the game.

        Returns:
            The removed GameConfiguration object.

        Raises:
            ValueError: If the host or game name does not exist.
        """
        confs = self._host_name_to_game_confs.get(host_name)
        if not confs:
            raise ValueError(f"No game configurations found for host {host_name}")

        # Find the game configuration by game_name
        game_to_remove = None
        for game in confs:
            if game.game_name == game_name:
                game_to_remove = game
                break

        if not game_to_remove:
            raise ValueError(f"Game {game_name} doesn't exist for host {host_name}")

        # Remove the game configuration from the host's set of configurations
        confs.remove(game_to_remove)

        # If the host has no more games, remove the host from the dictionary
        if not confs:
            del self._host_name_to_game_confs[host_name]

        # Remove the game configuration from the game → host mapping
        del self._game_conf_to_host_name[game_to_remove]

        return game_to_remove
