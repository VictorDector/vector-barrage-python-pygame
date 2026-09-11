"""Score storage for Vector Barrage.

This module owns parsing, ordering, migration, precedence and append behavior for
local score data. It contains no Pygame or screen dependencies and is designed
to be exercised against temporary files during QA.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import shutil

CANONICAL_SCORE_FILENAME = "scores.txt"
LEGACY_SCORE_FILENAME = "puntajes.txt"


@dataclass(frozen=True, slots=True)
class ScoreRecord:
    """One validated score record."""

    name: str
    score: int


@dataclass(frozen=True, slots=True)
class ScoreResolution:
    """Result of resolving the active score file."""

    path: Path
    source: str
    migrated: bool = False


def parse_score_line(line: str) -> ScoreRecord | None:
    """Parse one ``name,score`` line or return ``None`` when malformed."""

    raw_name, separator, raw_score = line.partition(",")
    if not separator:
        return None

    name = raw_name.strip()
    if not name:
        return None

    try:
        score = int(raw_score.strip())
    except ValueError:
        return None

    if score < 0:
        return None

    return ScoreRecord(name=name, score=score)


def read_scores(path: Path) -> list[ScoreRecord]:
    """Read valid records from ``path`` ordered by descending score."""

    if not path.exists():
        return []

    records: list[ScoreRecord] = []
    with path.open("r", encoding="utf-8-sig") as handle:
        for line in handle:
            record = parse_score_line(line)
            if record is not None:
                records.append(record)

    return sorted(records, key=lambda record: record.score, reverse=True)


def top_scores(path: Path, *, limit: int = 5) -> list[ScoreRecord]:
    """Return at most ``limit`` valid records in descending score order."""

    if limit < 0:
        raise ValueError("limit must be non-negative")
    return read_scores(path)[:limit]


def max_score(path: Path) -> int:
    """Return the highest valid score, or zero when none exist."""

    records = read_scores(path)
    return records[0].score if records else 0


def resolve_score_file(
    runtime_dir: Path,
    *,
    bundled_seed: Path | None = None,
) -> ScoreResolution:
    """Resolve canonical score storage with controlled legacy compatibility.

    Precedence:
    1. existing ``scores.txt``;
    2. migrate existing ``puntajes.txt`` to ``scores.txt`` when possible;
    3. if migration cannot be written, continue reading the legacy file;
    4. initialize ``scores.txt`` from ``bundled_seed`` when neither runtime
       file exists and a readable seed is supplied;
    5. otherwise return the canonical path without creating it.
    """

    runtime_dir = Path(runtime_dir)
    canonical = runtime_dir / CANONICAL_SCORE_FILENAME
    legacy = runtime_dir / LEGACY_SCORE_FILENAME

    if canonical.exists():
        return ScoreResolution(canonical, source="canonical")

    if legacy.exists():
        try:
            runtime_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(legacy, canonical)
        except OSError:
            return ScoreResolution(legacy, source="legacy_fallback")
        return ScoreResolution(canonical, source="legacy_migrated", migrated=True)

    if bundled_seed is not None:
        seed = Path(bundled_seed)
        if seed.is_file():
            try:
                runtime_dir.mkdir(parents=True, exist_ok=True)
                shutil.copy2(seed, canonical)
            except OSError:
                return ScoreResolution(canonical, source="canonical_uninitialized")
            return ScoreResolution(canonical, source="seed_initialized")

    return ScoreResolution(canonical, source="canonical_uninitialized")


def append_score(path: Path, name: str, score: int) -> ScoreRecord:
    """Append one validated score record to ``path`` exactly once per call."""

    normalized_name = name.strip()
    if not normalized_name:
        raise ValueError("name must not be empty or whitespace-only")
    if "," in normalized_name or "\n" in normalized_name or "\r" in normalized_name:
        raise ValueError("name must not contain commas or line breaks")
    if not isinstance(score, int) or isinstance(score, bool) or score < 0:
        raise ValueError("score must be a non-negative integer")

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    needs_separator = path.exists() and path.stat().st_size > 0
    if needs_separator:
        with path.open("rb") as handle:
            handle.seek(-1, 2)
            needs_separator = handle.read(1) not in {b"\n", b"\r"}

    with path.open("a", encoding="utf-8", newline="") as handle:
        if needs_separator:
            handle.write("\n")
        handle.write(f"{normalized_name},{score}\n")

    return ScoreRecord(name=normalized_name, score=score)
