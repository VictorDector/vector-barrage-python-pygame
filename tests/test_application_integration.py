"""Non-GUI integration contracts for the clean Vector Barrage application."""

from __future__ import annotations

from pathlib import Path

from vector_barrage.app import AppState, VectorBarrageApplication
from vector_barrage.gameplay.session import GameSessionResult, SessionOutcome
from vector_barrage.screens.about import AboutOutcome
from vector_barrage.screens.menu import MenuChoice
from vector_barrage.screens.name_entry import NameEntryResult
from vector_barrage.screens.scores import ScoresOutcome


class RecordingAudio:
    def __init__(self) -> None:
        self.events: list[str] = []

    def play_menu_music(self) -> None:
        self.events.append("menu_music")

    def play_gameplay_music(self) -> None:
        self.events.append("gameplay_music")

    def play_enemy_destroyed(self) -> None:
        self.events.append("enemy_destroyed")

    def play_new_record(self) -> None:
        self.events.append("new_record")

    def stop_music(self) -> None:
        self.events.append("stop_music")


class ScriptedMenu:
    def __init__(self, choices: list[MenuChoice]) -> None:
        self._choices = iter(choices)

    def run(self, _surface) -> MenuChoice:
        return next(self._choices)


class StaticScreen:
    def __init__(self, outcome) -> None:
        self.outcome = outcome
        self.calls = 0

    def run(self, _surface):
        self.calls += 1
        return self.outcome


class ScriptedGame:
    def __init__(self, result: GameSessionResult, *, emit_destroyed: bool = False) -> None:
        self.result = result
        self.emit_destroyed = emit_destroyed
        self.calls = 0

    def run(self, _surface, *, on_enemy_destroyed=None) -> GameSessionResult:
        self.calls += 1
        if self.emit_destroyed and on_enemy_destroyed is not None:
            on_enemy_destroyed(7)
        return self.result


class NameEntryHarness:
    def __init__(self, result: NameEntryResult) -> None:
        self.result = result
        self.calls = 0
        self.scores_seen: list[int] = []

    def factory(self, final_score: int):
        harness = self
        harness.scores_seen.append(final_score)

        class Screen:
            def run(self, _surface) -> NameEntryResult:
                harness.calls += 1
                return harness.result

        return Screen()


def test_integrated_flow_persists_completed_new_record_once(tmp_path: Path) -> None:
    score_path = tmp_path / "scores.txt"
    score_path.write_text("PLAYER_01,100\n", encoding="utf-8")
    audio = RecordingAudio()
    name_entry = NameEntryHarness(NameEntryResult(name="ACE"))

    app = VectorBarrageApplication(
        object(),
        score_path,
        audio=audio,
        menu_screen=ScriptedMenu(
            [MenuChoice.GAME, MenuChoice.SCORES, MenuChoice.ABOUT, MenuChoice.EXIT]
        ),
        scores_screen=StaticScreen(ScoresOutcome.RETURN_TO_MENU),
        about_screen=StaticScreen(AboutOutcome.RETURN_TO_MENU),
        game_session=ScriptedGame(
            GameSessionResult(
                final_score=120,
                outcome=SessionOutcome.RETURN_TO_MENU,
                completed=True,
            ),
            emit_destroyed=True,
        ),
        name_entry_factory=name_entry.factory,
    )

    assert app.run() is AppState.EXIT
    assert score_path.read_text(encoding="utf-8").splitlines().count("ACE,120") == 1
    assert name_entry.calls == 1
    assert name_entry.scores_seen == [120]
    assert "enemy_destroyed" in audio.events
    assert "new_record" in audio.events


def test_tied_score_does_not_open_name_entry_or_write(tmp_path: Path) -> None:
    score_path = tmp_path / "scores.txt"
    score_path.write_text("PLAYER_01,100\n", encoding="utf-8")
    name_entry = NameEntryHarness(NameEntryResult(name="SHOULD_NOT_WRITE"))

    app = VectorBarrageApplication(
        object(),
        score_path,
        menu_screen=ScriptedMenu([MenuChoice.GAME, MenuChoice.EXIT]),
        game_session=ScriptedGame(
            GameSessionResult(
                final_score=100,
                outcome=SessionOutcome.RETURN_TO_MENU,
                completed=True,
            )
        ),
        name_entry_factory=name_entry.factory,
    )

    assert app.run() is AppState.EXIT
    assert name_entry.calls == 0
    assert "SHOULD_NOT_WRITE" not in score_path.read_text(encoding="utf-8")


def test_cancelled_game_does_not_enter_record_flow(tmp_path: Path) -> None:
    score_path = tmp_path / "scores.txt"
    name_entry = NameEntryHarness(NameEntryResult(name="SHOULD_NOT_WRITE"))

    app = VectorBarrageApplication(
        object(),
        score_path,
        menu_screen=ScriptedMenu([MenuChoice.GAME, MenuChoice.EXIT]),
        game_session=ScriptedGame(
            GameSessionResult(
                final_score=999,
                outcome=SessionOutcome.RETURN_TO_MENU,
                completed=False,
            )
        ),
        name_entry_factory=name_entry.factory,
    )

    assert app.run() is AppState.EXIT
    assert name_entry.calls == 0
    assert not score_path.exists()


def test_cancelled_name_entry_does_not_write_score(tmp_path: Path) -> None:
    score_path = tmp_path / "scores.txt"
    score_path.write_text("PLAYER_01,100\n", encoding="utf-8")
    name_entry = NameEntryHarness(NameEntryResult())

    app = VectorBarrageApplication(
        object(),
        score_path,
        menu_screen=ScriptedMenu([MenuChoice.GAME, MenuChoice.EXIT]),
        game_session=ScriptedGame(
            GameSessionResult(
                final_score=150,
                outcome=SessionOutcome.RETURN_TO_MENU,
                completed=True,
            )
        ),
        name_entry_factory=name_entry.factory,
    )

    assert app.run() is AppState.EXIT
    assert name_entry.calls == 1
    assert score_path.read_text(encoding="utf-8") == "PLAYER_01,100\n"


def test_quit_from_name_entry_terminates_application(tmp_path: Path) -> None:
    name_entry = NameEntryHarness(NameEntryResult(quit_requested=True))
    app = VectorBarrageApplication(
        object(),
        tmp_path / "scores.txt",
        menu_screen=ScriptedMenu([MenuChoice.GAME]),
        game_session=ScriptedGame(
            GameSessionResult(
                final_score=10,
                outcome=SessionOutcome.RETURN_TO_MENU,
                completed=True,
            )
        ),
        name_entry_factory=name_entry.factory,
    )

    assert app.run() is AppState.EXIT


def test_quit_from_game_terminates_without_record_flow(tmp_path: Path) -> None:
    name_entry = NameEntryHarness(NameEntryResult(name="SHOULD_NOT_WRITE"))
    app = VectorBarrageApplication(
        object(),
        tmp_path / "scores.txt",
        menu_screen=ScriptedMenu([MenuChoice.GAME]),
        game_session=ScriptedGame(
            GameSessionResult(
                final_score=500,
                outcome=SessionOutcome.QUIT,
                completed=False,
            )
        ),
        name_entry_factory=name_entry.factory,
    )

    assert app.run() is AppState.EXIT
    assert name_entry.calls == 0
