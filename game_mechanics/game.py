from random import shuffle
from typing import Optional, Any

from game_mechanics.card_structures.card_structure import CardStructure
from game_mechanics.card_structures.trash import Trash
from game_mechanics.effects.effect import Effect
from game_mechanics.effects.game_setup import GameSetup
from game_mechanics.effects.game_stages.phase.end_game_phase import EndGamePhase
from game_mechanics.effects.game_stages.phase.phase import Phase
from game_mechanics.effects.game_stages.turn import Turn
from game_mechanics.effects.reactions.on_effect_reaction import Reaction
from game_mechanics.game_config.game_conf_consts import EMPTY_PILES_FOR_FINISH_BY_NUM_PLAYERS
from game_mechanics.game_status import GameStatus
from game_mechanics.game_supplies.all_cards import Card
from game_mechanics.player.player import Player
from game_mechanics.supply import Supply


class Game:
    """
    All changeable elements of the game would be here.
    """

    def __init__(self, game_conf):
        """
        Establish curr_player order.
        Initiate all the card structures that are part of the game.

        Args:
            game_conf: a "ready" dominion configuration.
        """
        self.game_conf = game_conf

        self.supply = Supply(
            kingdom_piles=self.game_conf.generate_supply_piles(self.game_conf.kingdom_piles_generators),
            standard_piles=self.game_conf.generate_supply_piles(self.game_conf.standard_piles_generators))
        self.trash = Trash(name="Trash")

        self.players: dict[str, Player] = {player_name: Player(cards=[], name=player_name) for player_name in
                                           self.game_conf.player_names}

        self._play_order: list[str] = list(self.players.keys())
        shuffle(self._play_order)

        self.curr_player_index = 0
        self._num_players = len(self.players)

        self.applied_effects: list[Effect] = []
        self.waiting_reactions: dict[str, list[Reaction]] = {pl: [] for pl in self.players.keys()}

        self.curr_phase: Optional[Phase] = None

    def __hash__(self):
        return hash(self.game_conf)

    @property
    def curr_player_name(self) -> str:
        return self._play_order[self.curr_player_index]

    @property
    def curr_player(self) -> Player:
        return self.players[self.curr_player_name]

    @property
    def player_list(self):
        return list(self.players.values())

    def get_playable_cards(self, struct: CardStructure, phase: Optional[Phase] = None):
        """
        Receives a card structure and returns all cards from it that can be played in the given phase.
        Default phase - current.
        """
        phase = phase if phase else self.curr_phase
        return [c for c in struct.cards if c.is_playable(phase)]

    def get_opponents_names_ordered(self, player_name: Optional[str] = None) -> list[str]:
        """
        Get all the opponents of a curr_player.
        If no curr_player name was supplied - returns the opponents of the current curr_player.

        Args:
            player_name: the curr_player's name

        Returns:
            A list of opponents (players) by the cycle order:
            from the player next to given player, up to the player before the given player.
        """
        player_name = player_name if player_name else self.curr_player_name
        all_player_names = self._play_order.copy()
        i = all_player_names.index(player_name)
        return all_player_names[i + 1:len(all_player_names)] + all_player_names[0:i]

    def get_opponents_ordered(self, player_name: Optional[str] = None) -> list[Player]:
        """
        Get all the opponents of a curr_player.
        If no curr_player name was supplied - returns the opponents of the current curr_player.

        Args:
            player_name: the curr_player's name

        Returns:
            A list of opponents (players).
        """
        return [self.players[opp] for opp in self.get_opponents_names_ordered(player_name)]

    def move_to_next_player(self):
        """
        Update next curr_player index.
        """
        self.curr_player_index = (self.curr_player_index + 1) % self._num_players

    def is_in_progress(self) -> bool:
        return self.game_conf.status == GameStatus.IN_PROGRESS

    async def run(self):
        """
        Run this game.
        """
        self.game_conf.status = GameStatus.IN_PROGRESS
        await self.apply_effect(GameSetup())
        while not self.game_over():
            await self.apply_effect(Turn(), self.curr_player)
        await self.apply_effect(EndGamePhase())

    async def apply_effect(self, effect: Effect, player: Optional[Player] = None, *args, **kwargs) -> Any:
        """
        Activate given effect and add it to the list.
        If a player is given - the effect would affect him.
        """
        self.applied_effects.append(effect)

        if player:
            reactions_to_apply = [reaction for reaction in self.waiting_reactions[player.name] if
                                  reaction.should_react(activated_effect=effect,
                                                        game=self,
                                                        player=player)]
            for reaction in reactions_to_apply:
                await self.apply_effect(reaction, player, *args, **kwargs)
        result = await effect.activate(self, player, *args, **kwargs)
        await self.send_player_views()
        return result

    def add_waiting_reaction(self, reaction: Reaction, player_name: str):
        self.waiting_reactions[player_name].append(reaction)

    def remove_waiting_reaction(self, reaction: Reaction, player_name: str):
        self.waiting_reactions[player_name].remove(reaction)

    def game_over(self, finishing_piles: tuple[str] = (Card.PROVINCE,)) -> bool:
        """
        Check whether any of the end conditions are met.
        """
        return self._is_enough_empty_piles() or self._is_any_of_finishing_piles_empty(finishing_piles)

    def _is_enough_empty_piles(self) -> bool:
        return self.supply.get_num_of_empty() >= EMPTY_PILES_FOR_FINISH_BY_NUM_PLAYERS[self._num_players]

    def _is_any_of_finishing_piles_empty(self, finishing_piles: tuple[str]) -> bool:
        empty_pile_names = [pile.name for pile in self.supply.empty_piles]
        for pile in finishing_piles:
            if pile in empty_pile_names:
                return True
        return False

    async def send_player_view(self, player_name: str):
        player = str(self.players[player_name])
        opponents = [str(opp) for opp in self.get_opponents_ordered(player_name)]
        message = f'Supply: {self.supply}. You: {player}. Opponents: {opponents}'
        await self.send_personal_message(message, player_name)

    async def send_player_views(self):
        for player_name in self.players.keys():
            await self.send_player_view(player_name)

    async def send_personal_message(self, message: str, player_name: str):
        await self.game_conf.ws_manager.send_personal_message(message, player_name)

    async def receive_text(self, player_name: str):
        return await self.game_conf.ws_manager.send_personal_message(player_name)
