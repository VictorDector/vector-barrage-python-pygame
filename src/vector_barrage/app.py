"""Integrated application runtime for Vector Barrage.

Application-level navigation, score persistence, new-record handling and audio
ownership are coordinated here. Screens and gameplay sessions return outcomes;
they never invoke one another.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from enum import Enum, auto
from pathlib import Path
import sys

from .audio import AudioService, NullAudioService, ProceduralAudioService
from .config import DEFAULT_CONFIG, PRODUCT_NAME
from .gameplay.rules import is_new_record
from .gameplay.session import GameSession, SessionOutcome
from .resources import read_only_resource_root, source_project_root
from .screens.about import AboutOutcome, AboutScreen
from .screens.menu import MainMenuScreen, MenuChoice
from .screens.name_entry import NameEntryScreen
from .screens.scores import ScoresOutcome, ScoresScreen
from .storage import (
    CANONICAL_SCORE_FILENAME,
    append_score,
    max_score,
    resolve_score_file,
)


class AppState(Enum):
    """Application-level states owned by the coordinator."""

    MENU = auto()
    GAME = auto()
    SCORES = auto()
    ABOUT = auto()
    EXIT = auto()


class AppAction(Enum):
    """Actions returned by active application handlers."""

    OPEN_GAME = auto()
    OPEN_SCORES = auto()
    OPEN_ABOUT = auto()
    RETURN_TO_MENU = auto()
    QUIT = auto()


StateHandler = Callable[[], AppAction]
NameEntryFactory = Callable[[int], NameEntryScreen]


_TRANSITIONS: dict[tuple[AppState, AppAction], AppState] = {
    (AppState.MENU, AppAction.OPEN_GAME): AppState.GAME,
    (AppState.MENU, AppAction.OPEN_SCORES): AppState.SCORES,
    (AppState.MENU, AppAction.OPEN_ABOUT): AppState.ABOUT,
    (AppState.MENU, AppAction.QUIT): AppState.EXIT,
    (AppState.GAME, AppAction.RETURN_TO_MENU): AppState.MENU,
    (AppState.GAME, AppAction.QUIT): AppState.EXIT,
    (AppState.SCORES, AppAction.RETURN_TO_MENU): AppState.MENU,
    (AppState.SCORES, AppAction.QUIT): AppState.EXIT,
    (AppState.ABOUT, AppAction.RETURN_TO_MENU): AppState.MENU,
    (AppState.ABOUT, AppAction.QUIT): AppState.EXIT,
}


def next_state(current: AppState, action: AppAction) -> AppState:
    """Resolve one allowed application transition."""

    try:
        return _TRANSITIONS[(current, action)]
    except KeyError as exc:
        raise ValueError(
            f"Unsupported application transition: {current.name} + {action.name}"
        ) from exc


def menu_choice_to_action(choice: MenuChoice) -> AppAction:
    """Translate one Main Menu choice to the application action contract."""

    mapping = {
        MenuChoice.GAME: AppAction.OPEN_GAME,
        MenuChoice.SCORES: AppAction.OPEN_SCORES,
        MenuChoice.ABOUT: AppAction.OPEN_ABOUT,
        MenuChoice.EXIT: AppAction.QUIT,
    }
    try:
        return mapping[choice]
    except KeyError as exc:
        raise ValueError(f"Unsupported Main Menu choice: {choice!r}") from exc


class ApplicationCoordinator:
    """Iteratively dispatch application states through injected handlers."""

    def __init__(
        self,
        handlers: Mapping[AppState, StateHandler],
        *,
        initial_state: AppState = AppState.MENU,
    ) -> None:
        if initial_state is AppState.EXIT:
            raise ValueError("The coordinator cannot start in EXIT.")
        self._handlers = dict(handlers)
        self._state = initial_state

    @property
    def state(self) -> AppState:
        """Return the currently active application state."""

        return self._state

    def step(self) -> AppState:
        """Execute exactly one active-state handler and apply one transition."""

        if self._state is AppState.EXIT:
            return AppState.EXIT

        try:
            handler = self._handlers[self._state]
        except KeyError as exc:
            raise RuntimeError(
                f"No handler registered for application state {self._state.name}."
            ) from exc

        action = handler()
        if not isinstance(action, AppAction):
            raise TypeError(
                f"Handler for {self._state.name} must return AppAction, "
                f"got {type(action).__name__}."
            )

        self._state = next_state(self._state, action)
        return self._state

    def run(self) -> AppState:
        """Run until EXIT using an iterative, non-recursive state loop."""

        while self._state is not AppState.EXIT:
            self.step()
        return self._state


class VectorBarrageApplication:
    """Wire public screens, gameplay, audio and persistence into one application."""

    def __init__(
        self,
        surface,
        score_path: Path,
        *,
        audio: AudioService | None = None,
        menu_screen: MainMenuScreen | None = None,
        scores_screen: ScoresScreen | None = None,
        about_screen: AboutScreen | None = None,
        game_session: GameSession | None = None,
        name_entry_factory: NameEntryFactory = NameEntryScreen,
        append_score_fn=append_score,
        max_score_fn=max_score,
    ) -> None:
        self.surface = surface
        self.score_path = Path(score_path)
        self.audio = audio or NullAudioService()
        self.menu_screen = menu_screen or MainMenuScreen()
        self.scores_screen = scores_screen or ScoresScreen(self.score_path)
        self.about_screen = about_screen or AboutScreen()
        self.game_session = game_session or GameSession()
        self.name_entry_factory = name_entry_factory
        self._append_score = append_score_fn
        self._max_score = max_score_fn

    def _handle_menu(self) -> AppAction:
        self.audio.play_menu_music()
        try:
            choice = self.menu_screen.run(self.surface)
        finally:
            self.audio.stop_music()
        return menu_choice_to_action(choice)

    def _handle_game(self) -> AppAction:
        self.audio.play_gameplay_music()
        try:
            result = self.game_session.run(
                self.surface,
                on_enemy_destroyed=lambda _enemy_id: self.audio.play_enemy_destroyed(),
            )
        finally:
            self.audio.stop_music()

        if result.outcome is SessionOutcome.QUIT:
            return AppAction.QUIT

        if result.completed and is_new_record(
            result.final_score,
            self._max_score(self.score_path),
        ):
            self.audio.play_new_record()
            try:
                name_result = self.name_entry_factory(result.final_score).run(self.surface)
            finally:
                self.audio.stop_music()

            if name_result.quit_requested:
                return AppAction.QUIT
            if name_result.name is not None:
                self._append_score(
                    self.score_path,
                    name_result.name,
                    result.final_score,
                )

        return AppAction.RETURN_TO_MENU

    def _handle_scores(self) -> AppAction:
        outcome = self.scores_screen.run(self.surface)
        return (
            AppAction.QUIT
            if outcome is ScoresOutcome.QUIT
            else AppAction.RETURN_TO_MENU
        )

    def _handle_about(self) -> AppAction:
        outcome = self.about_screen.run(self.surface)
        return (
            AppAction.QUIT
            if outcome is AboutOutcome.QUIT
            else AppAction.RETURN_TO_MENU
        )

    def handlers(self) -> dict[AppState, StateHandler]:
        """Return the complete runtime handler map."""

        return {
            AppState.MENU: self._handle_menu,
            AppState.GAME: self._handle_game,
            AppState.SCORES: self._handle_scores,
            AppState.ABOUT: self._handle_about,
        }

    def run(self) -> AppState:
        """Run the fully integrated application until Exit."""

        return ApplicationCoordinator(self.handlers()).run()


def runtime_score_directory(*, source_root: Path | None = None) -> Path:
    """Return the writable score directory for source or packaged execution."""

    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(source_root) if source_root is not None else source_project_root()


def bundled_seed_path() -> Path | None:
    """Return a bundled public score seed when one exists."""

    candidate = read_only_resource_root() / CANONICAL_SCORE_FILENAME
    return candidate if candidate.is_file() else None


def main() -> None:
    """Start the integrated Vector Barrage graphical application."""

    import pygame

    pygame.init()
    try:
        surface = pygame.display.set_mode(
            (DEFAULT_CONFIG.window_width, DEFAULT_CONFIG.window_height)
        )
        pygame.display.set_caption(PRODUCT_NAME)

        score_resolution = resolve_score_file(
            runtime_score_directory(),
            bundled_seed=bundled_seed_path(),
        )
        application = VectorBarrageApplication(
            surface,
            score_resolution.path,
            audio=ProceduralAudioService(),
        )
        application.run()
    finally:
        pygame.quit()
