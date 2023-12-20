from typing import Optional, Any

from game_mechanics.effects.effect import Effect


class AttackEffect(Effect):
    def __init__(self, attack_type: type[Effect], attack_conf: Optional[dict[str, Any]] = None):
        super().__init__()
        self.attack_type: type[Effect] = attack_type
        self.attack_conf = attack_conf if attack_conf else {}

    def apply(self, game, player=None, *args, **kwargs) -> Any:
        for pl in game.get_opponents_ordered():
            game.apply_effect(effect=self.attack_type(**self.attack_conf), player=pl)
