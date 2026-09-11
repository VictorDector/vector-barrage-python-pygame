"""Deterministic gameplay domain for Vector Barrage."""

from .model import (
    DEFAULT_GAMEPLAY_CONFIG,
    EnemyState,
    GameState,
    GameplayConfig,
    PlayerState,
    ProjectileState,
    Rect,
)
from .rules import (
    add_projectile,
    advance_level_if_cleared,
    apply_player_damage,
    is_new_record,
    move_player_horizontally,
    previous_maximum_or_zero,
    rectangles_overlap,
    resolve_projectile_enemy_collisions,
    wave_is_cleared,
)

__all__ = [
    "DEFAULT_GAMEPLAY_CONFIG",
    "EnemyState",
    "GameState",
    "GameplayConfig",
    "PlayerState",
    "ProjectileState",
    "Rect",
    "add_projectile",
    "advance_level_if_cleared",
    "apply_player_damage",
    "is_new_record",
    "move_player_horizontally",
    "previous_maximum_or_zero",
    "rectangles_overlap",
    "resolve_projectile_enemy_collisions",
    "wave_is_cleared",
]
