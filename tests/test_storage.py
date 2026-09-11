"""Contract tests for Vector Barrage score storage."""

from __future__ import annotations

from pathlib import Path

import pytest

from vector_barrage.storage import (
    CANONICAL_SCORE_FILENAME,
    LEGACY_SCORE_FILENAME,
    ScoreRecord,
    append_score,
    max_score,
    parse_score_line,
    read_scores,
    resolve_score_file,
    top_scores,
)


def test_parse_score_line_accepts_utf8_name_and_whitespace() -> None:
    assert parse_score_line("  María , 42  \n") == ScoreRecord("María", 42)


@pytest.mark.parametrize(
    "line",
    [
        "",
        "missing-separator",
        ",10",
        "PLAYER,not-a-number",
        "PLAYER,-1",
    ],
)
def test_parse_score_line_ignores_malformed_records(line: str) -> None:
    assert parse_score_line(line) is None


def test_read_scores_orders_descending_and_top_five(tmp_path: Path) -> None:
    score_file = tmp_path / CANONICAL_SCORE_FILENAME
    score_file.write_text(
        "A,10\nB,70\ninvalid\nC,30\nD,50\nE,20\nF,60\nG,40\n",
        encoding="utf-8",
    )

    assert [record.score for record in read_scores(score_file)] == [70, 60, 50, 40, 30, 20, 10]
    assert [record.name for record in top_scores(score_file)] == ["B", "F", "D", "G", "C"]
    assert max_score(score_file) == 70


def test_empty_or_invalid_file_has_zero_maximum(tmp_path: Path) -> None:
    score_file = tmp_path / CANONICAL_SCORE_FILENAME
    score_file.write_text("bad\nPLAYER,nope\n", encoding="utf-8")
    assert read_scores(score_file) == []
    assert max_score(score_file) == 0


def test_existing_canonical_file_has_precedence_over_legacy(tmp_path: Path) -> None:
    canonical = tmp_path / CANONICAL_SCORE_FILENAME
    legacy = tmp_path / LEGACY_SCORE_FILENAME
    canonical.write_text("CANONICAL,100\n", encoding="utf-8")
    legacy.write_text("LEGACY,999\n", encoding="utf-8")

    resolution = resolve_score_file(tmp_path)

    assert resolution.path == canonical
    assert resolution.source == "canonical"
    assert resolution.migrated is False
    assert canonical.read_text(encoding="utf-8") == "CANONICAL,100\n"
    assert legacy.read_text(encoding="utf-8") == "LEGACY,999\n"


def test_legacy_file_migrates_without_record_loss(tmp_path: Path) -> None:
    legacy = tmp_path / LEGACY_SCORE_FILENAME
    legacy.write_text("LEGACY_1,75\nLEGACY_2,25\n", encoding="utf-8")

    resolution = resolve_score_file(tmp_path)
    canonical = tmp_path / CANONICAL_SCORE_FILENAME

    assert resolution.path == canonical
    assert resolution.source == "legacy_migrated"
    assert resolution.migrated is True
    assert canonical.read_text(encoding="utf-8") == legacy.read_text(encoding="utf-8")
    assert legacy.exists()


def test_seed_initializes_only_when_runtime_data_is_absent(tmp_path: Path) -> None:
    seed = tmp_path / "seed.txt"
    runtime = tmp_path / "runtime"
    seed.write_text("PLAYER_01,500\nPLAYER_02,350\n", encoding="utf-8")

    resolution = resolve_score_file(runtime, bundled_seed=seed)
    canonical = runtime / CANONICAL_SCORE_FILENAME

    assert resolution.path == canonical
    assert resolution.source == "seed_initialized"
    assert canonical.read_text(encoding="utf-8") == seed.read_text(encoding="utf-8")

    canonical.write_text("USER_SCORE,800\n", encoding="utf-8")
    second = resolve_score_file(runtime, bundled_seed=seed)
    assert second.source == "canonical"
    assert canonical.read_text(encoding="utf-8") == "USER_SCORE,800\n"


def test_append_score_validates_name_and_preserves_line_boundary(tmp_path: Path) -> None:
    score_file = tmp_path / CANONICAL_SCORE_FILENAME
    score_file.write_text("PLAYER_01,500", encoding="utf-8")

    appended = append_score(score_file, "  NEW_PLAYER  ", 625)

    assert appended == ScoreRecord("NEW_PLAYER", 625)
    assert score_file.read_text(encoding="utf-8") == "PLAYER_01,500\nNEW_PLAYER,625\n"


@pytest.mark.parametrize("name", ["", "   ", "A,B", "A\nB", "A\rB"])
def test_append_score_rejects_unsafe_names(tmp_path: Path, name: str) -> None:
    with pytest.raises(ValueError):
        append_score(tmp_path / CANONICAL_SCORE_FILENAME, name, 10)


@pytest.mark.parametrize("score", [-1, 1.5, True])
def test_append_score_rejects_invalid_scores(tmp_path: Path, score: object) -> None:
    with pytest.raises(ValueError):
        append_score(tmp_path / CANONICAL_SCORE_FILENAME, "PLAYER", score)  # type: ignore[arg-type]


def test_qa_uses_only_temporary_score_files(tmp_path: Path) -> None:
    score_file = tmp_path / CANONICAL_SCORE_FILENAME
    append_score(score_file, "TEMP_PLAYER", 123)
    assert score_file.parent == tmp_path
    assert read_scores(score_file) == [ScoreRecord("TEMP_PLAYER", 123)]
