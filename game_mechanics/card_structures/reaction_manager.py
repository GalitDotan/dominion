from typing import Callable

from game_mechanics.effects.effect import Effect
from game_mechanics.effects.reactions.on_effect_reaction import Reaction


class ReactionWaiter:
    def __init__(self, player_reaction_manager: 'PlayerReactionManager',
                 reaction: Reaction,
                 enabling_effect_type: type[Effect],
                 disabling_effect_type: type[Effect],
                 enabling_condition: Callable[[Effect], bool],
                 disabling_condition: Callable[[Effect], bool]):
        self.reaction: Reaction = reaction

        self.enabling_effect: type[Effect] = enabling_effect_type
        self.disabling_effect: type[Effect] = disabling_effect_type

        self.enabling_condition: Callable[[Effect], bool] = enabling_condition
        self.disabling_condition: Callable[[Effect], bool] = disabling_condition

        self.player_reaction_manager: 'PlayerReactionManager' = player_reaction_manager

    def remove(self):
        self.player_reaction_manager.enabling_effect_to_reaction[self.enabling_effect].remove(self)
        self.player_reaction_manager.disabling_effect_to_reaction[self.disabling_effect].remove(self)


def _upsert(reaction_waiter: ReactionWaiter, dict_to_update: dict[type[Effect], list[ReactionWaiter]],
            key: type[Effect]):
    lst = dict_to_update.get(key, [])
    lst.append(reaction_waiter)
    dict_to_update[key] = lst


class PlayerReactionManager:
    def __init__(self, player_name: str):
        self.player_name: str = player_name
        self.enabling_effect_to_reaction: dict[type[Effect], list[ReactionWaiter]] = {}
        self.disabling_effect_to_reaction: dict[type[Effect], list[ReactionWaiter]] = {}

    def add_reaction(self, reaction_waiter: ReactionWaiter):
        _upsert(reaction_waiter=reaction_waiter, dict_to_update=self.enabling_effect_to_reaction,
                key=reaction_waiter.enabling_effect)
        _upsert(reaction_waiter=reaction_waiter, dict_to_update=self.disabling_effect_to_reaction,
                key=reaction_waiter.disabling_effect)

    def remove_reaction(self, reaction_waiter: ReactionWaiter):
        reaction_waiter.remove()

    async def before_effect_appliance(self, activated_effect: Effect, game):
        await self.enable_reactions(activated_effect, game)
        self.disable_reactions(activated_effect)

    async def enable_reactions(self, activated_effect: Effect, game):
        for effect_type, waiting_reactions in self.enabling_effect_to_reaction.items():
            if type(activated_effect) is effect_type:
                for waiting_reaction in waiting_reactions:
                    if waiting_reaction.enabling_condition(activated_effect):
                        await game.apply_effect(effect=self, player=game.players[self.player_name])

    def disable_reactions(self, activated_effect: Effect):
        for effect_type, waiting_reactions in self.disabling_effect_to_reaction.items():
            if type(activated_effect) is effect_type:
                for waiting_reaction in waiting_reactions:
                    if waiting_reaction.disabling_condition(activated_effect):
                        waiting_reaction.remove()
