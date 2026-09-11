"""Contracts for the synthetic public Vector Barrage score seed."""

from __future__ import annotations

from pathlib import Path

from vector_barrage.storage import ScoreRecord, max_score, read_scores, top_scores


EXPECTED_PUBLIC_SEED = [
    ScoreRecord("PLAYER_01", 500),
    ScoreRecord("PLAYER_02", 350),
    ScoreRecord("PLAYER_03", 250),
    ScoreRecord("PLAYER_04", 150),
    ScoreRecord("PLAYER_05", 100),
]


def public_seed_path() -> Path:
    return Path(__file__).resolve().parents[1] / "scores.txt"


def test_public_seed_contains_only_synthetic_player_identifiers() -> None:
    records = read_scores(public_seed_path())
    assert records == EXPECTED_PUBLIC_SEED
    assert all(record.name.startswith("PLAYER_") for record in records)


def test_public_seed_has_exactly_five_unique_records() -> None:
    records = read_scores(public_seed_path())
    assert len(records) == 5
    assert len({record.name for record in records}) == 5
    assert len({record.score for record in records}) == 5


def test_public_seed_is_already_sorted_descending() -> None:
    records = read_scores(public_seed_path())
    assert [record.score for record in records] == [500, 350, 250, 150, 100]
    assert top_scores(public_seed_path()) == EXPECTED_PUBLIC_SEED
    assert max_score(public_seed_path()) == 500


def test_public_seed_contains_no_historical_person_names() -> None:
    text = public_seed_path().read_text(encoding="utf-8")
    forbidden = {
        "Victor Dector",
        "María Torres",
        "Carlos López",
        "Laura Martínez",
        "Roberto Sánchez",
        "Ana Gómez",
        "Javier Rodríguez",
        "Sofia Hernández",
        "Diego Ramírez",
        "Natalia García",
        "Andrés Díaz",
    }
    assert all(name not in text for name in forbidden)
