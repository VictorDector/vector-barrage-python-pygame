"""Deterministic collision and movement contract tests."""

from __future__ import annotations

import pytest

from vector_barrage.gameplay import (
    EnemyState,
    GameState,
    GameplayConfig,
    PlayerState,
    ProjectileState,
    Rect,
    add_projectile,
    move_player_horizontally,
    rectangles_overlap,
    resolve_projectile_enemy_collisions,
)


def _base_state(
    *,
    enemies: tuple[EnemyState, ...] = (),
    projectiles: tuple[ProjectileState, ...] = (),
    score: int = 0,
) -> GameState:
    return GameState(
        player=PlayerState(Rect(100, 500, 40, 24)),
        enemies=enemies,
        projectiles=projectiles,
        score=score,
    )


def test_rectangles_overlap_requires_positive_intersection() -> None:
    a = Rect(10, 10, 20, 20)
    assert rectangles_overlap(a, Rect(20, 20, 20, 20)) is True
    assert rectangles_overlap(a, Rect(30, 10, 20, 20)) is False
    assert rectangles_overlap(a, Rect(10, 30, 20, 20)) is False


def test_player_horizontal_motion_is_clamped_to_playfield() -> None:
    player = PlayerState(Rect(10, 500, 40, 24))

    assert move_player_horizontally(player, -50).rect.x == 0
    assert move_player_horizontally(player, 900, playfield_width=800).rect.x == 760
    assert move_player_horizontally(player, 25).rect.x == 35


def test_player_motion_rejects_impossible_playfield() -> None:
    player = PlayerState(Rect(0, 0, 40, 24))
    with pytest.raises(ValueError):
        move_player_horizontally(player, 1, playfield_width=20)


def test_add_projectile_requires_unique_active_identifier() -> None:
    projectile = ProjectileState(1, Rect(100, 450, 4, 12))
    state = add_projectile(_base_state(), projectile)
    assert state.projectiles == (projectile,)

    with pytest.raises(ValueError):
        add_projectile(state, projectile)

    with pytest.raises(ValueError):
        add_projectile(_base_state(), ProjectileState(2, Rect(0, 0, 4, 12), active=False))


def test_confirmed_collision_destroys_once_and_scores_once() -> None:
    enemy = EnemyState(7, Rect(100, 100, 30, 20))
    projectile = ProjectileState(4, Rect(110, 105, 4, 12))
    config = GameplayConfig(kill_score=25)

    resolved, destroyed = resolve_projectile_enemy_collisions(
        _base_state(enemies=(enemy,), projectiles=(projectile,), score=50),
        config=config,
    )

    assert destroyed == (7,)
    assert resolved.score == 75
    assert resolved.enemies[0].alive is False
    assert resolved.projectiles[0].active is False

    repeated, destroyed_again = resolve_projectile_enemy_collisions(resolved, config=config)
    assert destroyed_again == ()
    assert repeated.score == 75


def test_one_projectile_can_destroy_at_most_one_enemy_per_resolution() -> None:
    enemies = (
        EnemyState(1, Rect(100, 100, 30, 20)),
        EnemyState(2, Rect(100, 100, 30, 20)),
    )
    projectile = ProjectileState(1, Rect(110, 105, 4, 12))

    resolved, destroyed = resolve_projectile_enemy_collisions(
        _base_state(enemies=enemies, projectiles=(projectile,))
    )

    assert destroyed == (1,)
    assert resolved.score == 10
    assert [enemy.alive for enemy in resolved.enemies] == [False, True]


def test_two_projectiles_can_destroy_two_distinct_enemies() -> None:
    enemies = (
        EnemyState(1, Rect(100, 100, 30, 20)),
        EnemyState(2, Rect(200, 100, 30, 20)),
    )
    projectiles = (
        ProjectileState(1, Rect(110, 105, 4, 12)),
        ProjectileState(2, Rect(210, 105, 4, 12)),
    )

    resolved, destroyed = resolve_projectile_enemy_collisions(
        _base_state(enemies=enemies, projectiles=projectiles)
    )

    assert destroyed == (1, 2)
    assert resolved.score == 20
    assert all(not enemy.alive for enemy in resolved.enemies)
    assert all(not projectile.active for projectile in resolved.projectiles)


def test_non_collision_preserves_state_and_score() -> None:
    enemy = EnemyState(1, Rect(300, 100, 30, 20))
    projectile = ProjectileState(1, Rect(100, 100, 4, 12))
    state = _base_state(enemies=(enemy,), projectiles=(projectile,), score=40)

    resolved, destroyed = resolve_projectile_enemy_collisions(state)

    assert destroyed == ()
    assert resolved == state
