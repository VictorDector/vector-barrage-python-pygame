"""Deterministic scoring and progression contract tests."""

from __future__ import annotations

import pytest

from vector_barrage.gameplay import (
    EnemyState,
    GameState,
    PlayerState,
    Rect,
    advance_level_if_cleared,
    apply_player_damage,
    is_new_record,
    previous_maximum_or_zero,
    wave_is_cleared,
)


def _state(*, lives: int = 3, level: int = 1, enemies: tuple[EnemyState, ...] = ()) -> GameState:
    return GameState(
        player=PlayerState(Rect(100, 500, 40, 24), lives=lives),
        enemies=enemies,
        level=level,
    )


def test_strict_new_record_requires_greater_score() -> None:
    assert is_new_record(101, 100) is True
    assert is_new_record(100, 100) is False
    assert is_new_record(99, 100) is False


@pytest.mark.parametrize(("final_score", "previous"), [(-1, 0), (0, -1)])
def test_new_record_rejects_negative_scores(final_score: int, previous: int) -> None:
    with pytest.raises(ValueError):
        is_new_record(final_score, previous)


def test_previous_maximum_defaults_to_zero_and_ignores_invalid_values() -> None:
    assert previous_maximum_or_zero([]) == 0
    assert previous_maximum_or_zero([10, 70, -1, 40, True]) == 70


def test_player_damage_reduces_lives_without_premature_game_over() -> None:
    damaged = apply_player_damage(_state(lives=3))
    assert damaged.player.lives == 2
    assert damaged.game_over is False


def test_player_damage_sets_game_over_at_zero_lives() -> None:
    damaged = apply_player_damage(_state(lives=1))
    assert damaged.player.lives == 0
    assert damaged.game_over is True


def test_damage_after_game_over_is_idempotent() -> None:
    ended = apply_player_damage(_state(lives=1))
    assert apply_player_damage(ended) == ended


def test_damage_amount_must_be_positive() -> None:
    with pytest.raises(ValueError):
        apply_player_damage(_state(), amount=0)


def test_wave_clear_requires_existing_wave_and_no_living_enemy() -> None:
    living = EnemyState(1, Rect(10, 10, 20, 20), alive=True)
    defeated = EnemyState(2, Rect(40, 10, 20, 20), alive=False)

    assert wave_is_cleared(_state(enemies=())) is False
    assert wave_is_cleared(_state(enemies=(living, defeated))) is False
    assert wave_is_cleared(_state(enemies=(defeated,))) is True


def test_cleared_wave_advances_level_exactly_once_until_next_wave_exists() -> None:
    defeated = EnemyState(1, Rect(10, 10, 20, 20), alive=False)
    state = _state(level=4, enemies=(defeated,))

    advanced = advance_level_if_cleared(state)
    assert advanced.level == 5
    assert advanced.enemies == ()

    second = advance_level_if_cleared(advanced)
    assert second.level == 5


def test_game_over_state_does_not_advance_level() -> None:
    defeated = EnemyState(1, Rect(10, 10, 20, 20), alive=False)
    ended = apply_player_damage(_state(lives=1, level=2, enemies=(defeated,)))
    assert advance_level_if_cleared(ended).level == 2
