"""Deterministic gameplay rules for Vector Barrage."""

from __future__ import annotations

from dataclasses import replace

from .model import (
    DEFAULT_GAMEPLAY_CONFIG,
    EnemyState,
    GameState,
    GameplayConfig,
    PlayerState,
    ProjectileState,
    Rect,
)


def rectangles_overlap(a: Rect, b: Rect) -> bool:
    """Return True when two axis-aligned rectangles overlap."""

    return (
        a.x < b.x + b.width
        and a.x + a.width > b.x
        and a.y < b.y + b.height
        and a.y + a.height > b.y
    )


def move_player_horizontally(
    player: PlayerState,
    delta_x: float,
    *,
    playfield_width: float = DEFAULT_GAMEPLAY_CONFIG.playfield_width,
) -> PlayerState:
    """Move the player horizontally while clamping to the playfield."""

    if playfield_width < player.rect.width:
        raise ValueError("playfield_width must be at least the player width")

    max_x = playfield_width - player.rect.width
    new_x = min(max(player.rect.x + delta_x, 0.0), max_x)
    return replace(player, rect=replace(player.rect, x=new_x))


def add_projectile(state: GameState, projectile: ProjectileState) -> GameState:
    """Add one active projectile with a unique identifier."""

    if not projectile.active:
        raise ValueError("new projectile must be active")
    if any(existing.projectile_id == projectile.projectile_id for existing in state.projectiles):
        raise ValueError("projectile_id must be unique")
    return replace(state, projectiles=(*state.projectiles, projectile))


def resolve_projectile_enemy_collisions(
    state: GameState,
    *,
    config: GameplayConfig = DEFAULT_GAMEPLAY_CONFIG,
) -> tuple[GameState, tuple[int, ...]]:
    """Resolve projectile/enemy hits once and return destroyed enemy IDs.

    Each active projectile can consume at most one living enemy per resolution
    pass. Destroyed enemies and consumed projectiles become inactive, so calling
    this function again with the returned state cannot double-score the same hit.
    """

    enemies = list(state.enemies)
    projectiles = list(state.projectiles)
    destroyed_ids: list[int] = []
    score = state.score

    for projectile_index, projectile in enumerate(projectiles):
        if not projectile.active:
            continue

        for enemy_index, enemy in enumerate(enemies):
            if not enemy.alive:
                continue
            if not rectangles_overlap(projectile.rect, enemy.rect):
                continue

            projectiles[projectile_index] = replace(projectile, active=False)
            enemies[enemy_index] = replace(enemy, alive=False)
            destroyed_ids.append(enemy.enemy_id)
            score += config.kill_score
            break

    return (
        replace(
            state,
            enemies=tuple(enemies),
            projectiles=tuple(projectiles),
            score=score,
        ),
        tuple(destroyed_ids),
    )


def apply_player_damage(state: GameState, *, amount: int = 1) -> GameState:
    """Reduce player lives and set game-over exactly when lives reach zero."""

    if amount <= 0:
        raise ValueError("damage amount must be positive")
    if state.game_over:
        return state

    remaining_lives = max(state.player.lives - amount, 0)
    return replace(
        state,
        player=replace(state.player, lives=remaining_lives),
        game_over=remaining_lives == 0,
    )


def wave_is_cleared(state: GameState) -> bool:
    """Return True when the current wave contains no living enemies."""

    return bool(state.enemies) and all(not enemy.alive for enemy in state.enemies)


def advance_level_if_cleared(state: GameState) -> GameState:
    """Advance exactly one level after a cleared wave.

    Enemy creation belongs to the runtime/session layer. This rule only advances
    the deterministic level counter; the session is responsible for supplying
    the next wave before invoking progression again.
    """

    if state.game_over or not wave_is_cleared(state):
        return state
    return replace(state, level=state.level + 1, enemies=())


def previous_maximum_or_zero(scores: tuple[int, ...] | list[int]) -> int:
    """Return the highest non-negative score, or zero for no valid scores."""

    valid = [score for score in scores if isinstance(score, int) and not isinstance(score, bool) and score >= 0]
    return max(valid, default=0)


def is_new_record(final_score: int, previous_max_score: int) -> bool:
    """Apply the strict public new-record rule: final score must be greater."""

    if final_score < 0 or previous_max_score < 0:
        raise ValueError("scores must be non-negative")
    return final_score > previous_max_score
