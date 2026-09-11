"""Deterministic gameplay state for Vector Barrage."""

from __future__ import annotations

from dataclasses import dataclass, replace


@dataclass(frozen=True, slots=True)
class Rect:
    """Axis-aligned rectangle used by deterministic collision rules."""

    x: float
    y: float
    width: float
    height: float

    def moved(self, *, dx: float = 0.0, dy: float = 0.0) -> "Rect":
        return replace(self, x=self.x + dx, y=self.y + dy)


@dataclass(frozen=True, slots=True)
class PlayerState:
    rect: Rect
    lives: int = 3


@dataclass(frozen=True, slots=True)
class EnemyState:
    enemy_id: int
    rect: Rect
    alive: bool = True


@dataclass(frozen=True, slots=True)
class ProjectileState:
    projectile_id: int
    rect: Rect
    active: bool = True


@dataclass(frozen=True, slots=True)
class GameState:
    """Pure gameplay state with no rendering or filesystem concerns."""

    player: PlayerState
    enemies: tuple[EnemyState, ...]
    projectiles: tuple[ProjectileState, ...] = ()
    score: int = 0
    level: int = 1
    game_over: bool = False


@dataclass(frozen=True, slots=True)
class GameplayConfig:
    """Independent gameplay tuning values for the public implementation."""

    playfield_width: float = 800.0
    playfield_height: float = 600.0
    kill_score: int = 10
    starting_lives: int = 3


DEFAULT_GAMEPLAY_CONFIG = GameplayConfig()
