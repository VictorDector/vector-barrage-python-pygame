"""Contract tests for Pygame-independent runtime/session mechanics."""

from __future__ import annotations

from dataclasses import replace

import pytest

from vector_barrage.gameplay.model import EnemyState, ProjectileState, Rect
from vector_barrage.gameplay.session import (
    DEFAULT_SESSION_TUNING,
    advance_runtime_state,
    create_enemy_wave,
    create_initial_state,
    create_player_projectile,
    move_active_projectiles,
    move_enemy_formation,
)


def test_initial_state_has_centered_player_and_complete_wave() -> None:
    state = create_initial_state()
    assert state.level == 1
    assert state.score == 0
    assert state.player.lives == 3
    assert len(state.enemies) == (
        DEFAULT_SESSION_TUNING.enemy_columns * DEFAULT_SESSION_TUNING.enemy_rows
    )
    assert state.player.rect.x == pytest.approx(
        (800 - DEFAULT_SESSION_TUNING.player_width) / 2
    )


def test_create_enemy_wave_uses_unique_ids() -> None:
    wave = create_enemy_wave(1)
    assert len({enemy.enemy_id for enemy in wave}) == len(wave)


def test_projectile_starts_centered_above_player() -> None:
    state = create_initial_state()
    projectile = create_player_projectile(state, 7)
    assert projectile.projectile_id == 7
    assert projectile.rect.x + projectile.rect.width / 2 == pytest.approx(
        state.player.rect.x + state.player.rect.width / 2
    )
    assert projectile.rect.y + projectile.rect.height == pytest.approx(state.player.rect.y)


def test_projectile_movement_discards_expired_projectiles() -> None:
    state = create_initial_state()
    state = replace(
        state,
        projectiles=(
            ProjectileState(1, Rect(10, 2, 4, 14)),
            ProjectileState(2, Rect(20, 200, 4, 14)),
        ),
    )
    advanced = move_active_projectiles(state, 0.1)
    assert [projectile.projectile_id for projectile in advanced.projectiles] == [2]
    assert advanced.projectiles[0].rect.y < 200


def test_enemy_formation_reverses_and_drops_at_edge() -> None:
    enemy = EnemyState(1, Rect(765, 50, 36, 24))
    motion = move_enemy_formation((enemy,), 1, 0.1)
    assert motion.direction == -1
    assert motion.enemies[0].rect.x == enemy.rect.x
    assert motion.enemies[0].rect.y == enemy.rect.y + DEFAULT_SESSION_TUNING.enemy_drop


def test_enemy_formation_speed_increases_by_level() -> None:
    enemy = EnemyState(1, Rect(100, 50, 36, 24))
    level_1 = move_enemy_formation((enemy,), 1, 0.5, level=1)
    level_3 = move_enemy_formation((enemy,), 1, 0.5, level=3)
    assert level_3.enemies[0].rect.x > level_1.enemies[0].rect.x


def test_breach_reduces_one_life_and_resets_wave() -> None:
    state = create_initial_state()
    breach_enemy = EnemyState(1, Rect(100, state.player.rect.y - 10, 36, 24))
    state = replace(state, enemies=(breach_enemy,), projectiles=())
    advanced, direction, destroyed = advance_runtime_state(
        state,
        0.0,
        enemy_direction=1,
    )
    assert advanced.player.lives == 2
    assert advanced.game_over is False
    assert len(advanced.enemies) == (
        DEFAULT_SESSION_TUNING.enemy_columns * DEFAULT_SESSION_TUNING.enemy_rows
    )
    assert direction == 1
    assert destroyed == ()


def test_final_breach_sets_game_over_without_spawning_new_wave() -> None:
    state = create_initial_state()
    state = replace(
        state,
        player=replace(state.player, lives=1),
        enemies=(EnemyState(1, Rect(100, state.player.rect.y - 5, 36, 24)),),
    )
    advanced, _, _ = advance_runtime_state(state, 0.0, enemy_direction=1)
    assert advanced.player.lives == 0
    assert advanced.game_over is True
    assert len(advanced.enemies) == 1


def test_collision_scores_then_wave_advances_and_respawns() -> None:
    state = create_initial_state()
    enemy = EnemyState(1, Rect(100, 100, 36, 24))
    projectile = ProjectileState(1, Rect(110, 108, 4, 14))
    state = replace(state, enemies=(enemy,), projectiles=(projectile,))
    advanced, direction, destroyed = advance_runtime_state(
        state,
        0.0,
        enemy_direction=1,
    )
    assert destroyed == (1,)
    assert advanced.score == 10
    assert advanced.level == 2
    assert len(advanced.enemies) == (
        DEFAULT_SESSION_TUNING.enemy_columns * DEFAULT_SESSION_TUNING.enemy_rows
    )
    assert direction == 1


def test_invalid_enemy_direction_is_rejected() -> None:
    with pytest.raises(ValueError):
        move_enemy_formation(create_enemy_wave(1), 0, 0.1)


def test_negative_elapsed_time_is_rejected() -> None:
    state = create_initial_state()
    with pytest.raises(ValueError):
        move_active_projectiles(state, -0.1)


def test_destroyed_breaching_enemy_does_not_remove_life() -> None:
    state = create_initial_state()
    enemy = EnemyState(1, Rect(100, state.player.rect.y - 10, 36, 24))
    projectile = ProjectileState(1, Rect(110, state.player.rect.y, 4, 14))
    state = replace(state, enemies=(enemy,), projectiles=(projectile,))
    advanced, _, destroyed = advance_runtime_state(state, 0.0, enemy_direction=1)
    assert destroyed == (1,)
    assert advanced.player.lives == 3
    assert advanced.level == 2
