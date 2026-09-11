"""Contract tests for application-level navigation."""

from __future__ import annotations

import pytest

from vector_barrage.app import (
    AppAction,
    AppState,
    ApplicationCoordinator,
    next_state,
)


@pytest.mark.parametrize(
    ("action", "expected"),
    [
        (AppAction.OPEN_GAME, AppState.GAME),
        (AppAction.OPEN_SCORES, AppState.SCORES),
        (AppAction.OPEN_ABOUT, AppState.ABOUT),
        (AppAction.QUIT, AppState.EXIT),
    ],
)
def test_main_menu_routes_to_allowed_states(
    action: AppAction,
    expected: AppState,
) -> None:
    assert next_state(AppState.MENU, action) is expected


@pytest.mark.parametrize("state", [AppState.GAME, AppState.SCORES, AppState.ABOUT])
def test_secondary_states_return_to_menu(state: AppState) -> None:
    assert next_state(state, AppAction.RETURN_TO_MENU) is AppState.MENU


def test_invalid_cross_screen_transition_is_rejected() -> None:
    with pytest.raises(ValueError):
        next_state(AppState.SCORES, AppAction.OPEN_ABOUT)


def test_coordinator_dispatches_one_handler_per_step() -> None:
    calls: list[AppState] = []

    def menu_handler() -> AppAction:
        calls.append(AppState.MENU)
        return AppAction.OPEN_ABOUT

    def about_handler() -> AppAction:
        calls.append(AppState.ABOUT)
        return AppAction.RETURN_TO_MENU

    coordinator = ApplicationCoordinator(
        {
            AppState.MENU: menu_handler,
            AppState.ABOUT: about_handler,
        }
    )

    assert coordinator.step() is AppState.ABOUT
    assert coordinator.step() is AppState.MENU
    assert calls == [AppState.MENU, AppState.ABOUT]


def test_repeated_navigation_uses_iterative_coordinator_loop() -> None:
    cycles = 2_000
    menu_visits = 0
    about_visits = 0

    def menu_handler() -> AppAction:
        nonlocal menu_visits
        menu_visits += 1
        if menu_visits > cycles:
            return AppAction.QUIT
        return AppAction.OPEN_ABOUT

    def about_handler() -> AppAction:
        nonlocal about_visits
        about_visits += 1
        return AppAction.RETURN_TO_MENU

    coordinator = ApplicationCoordinator(
        {
            AppState.MENU: menu_handler,
            AppState.ABOUT: about_handler,
        }
    )

    assert coordinator.run() is AppState.EXIT
    assert menu_visits == cycles + 1
    assert about_visits == cycles
