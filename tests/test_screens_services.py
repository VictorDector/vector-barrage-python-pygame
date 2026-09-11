"""Non-GUI contract tests for screens and public infrastructure services."""

from __future__ import annotations

import pytest

from vector_barrage.audio import NullAudioService
from vector_barrage.config import AUTHOR_NAME, PRODUCT_NAME, PUBLIC_GITHUB_URL
from vector_barrage.links import validate_public_url
from vector_barrage.screens.about import about_lines, wrap_text_to_width
from vector_barrage.screens.menu import MenuChoice, menu_choice_for_index
from vector_barrage.screens.name_entry import NameEntryResult, normalize_player_name
from vector_barrage.screens.scores import format_score_rows
from vector_barrage.storage import ScoreRecord


def test_menu_indices_map_to_exact_public_actions() -> None:
    assert [menu_choice_for_index(index) for index in range(4)] == [
        MenuChoice.GAME,
        MenuChoice.SCORES,
        MenuChoice.ABOUT,
        MenuChoice.EXIT,
    ]


def test_menu_rejects_out_of_range_index() -> None:
    with pytest.raises(ValueError):
        menu_choice_for_index(4)


def test_score_rows_preserve_order_and_format_numeric_values() -> None:
    rows = format_score_rows(
        [
            ScoreRecord("PLAYER_01", 500),
            ScoreRecord("PLAYER_02", 350),
        ]
    )
    assert rows[0].startswith(" 1. PLAYER_01")
    assert rows[0].endswith("500")
    assert rows[1].startswith(" 2. PLAYER_02")
    assert rows[1].endswith("350")


def test_about_copy_uses_public_identity() -> None:
    copy = "\n".join(about_lines())
    assert PRODUCT_NAME in copy
    assert AUTHOR_NAME in copy
    assert "Hybridge" not in copy
    assert "Space Invaders" not in copy


def test_about_copy_uses_factual_generated_media_wording() -> None:
    copy = "\n".join(about_lines())
    assert "medios generados" in copy
    assert "redistribuibles" not in copy

    class FixedWidthFont:
        @staticmethod
        def size(text: str) -> tuple[int, int]:
            return len(text) * 12, 30

    font = FixedWidthFont()
    max_width = 680
    wrapped_groups = [
        wrap_text_to_width(paragraph, font, max_width)
        for paragraph in about_lines()[1:]
    ]

    assert any(len(group) > 1 for group in wrapped_groups)
    assert all(
        font.size(line)[0] <= max_width
        for group in wrapped_groups
        for line in group
    )
    assert [" ".join(group) for group in wrapped_groups] == list(about_lines()[1:])


def test_approved_github_link_is_https() -> None:
    assert validate_public_url(PUBLIC_GITHUB_URL) == PUBLIC_GITHUB_URL


@pytest.mark.parametrize(
    "url",
    [
        "",
        "http://example.com",
        "javascript:alert(1)",
        "https://user:pass@example.com/private",
        "github.com/VictorDector/vector-barrage-python-pygame",
    ],
)
def test_public_link_validation_rejects_unsafe_or_non_https_values(url: str) -> None:
    with pytest.raises(ValueError):
        validate_public_url(url)


def test_name_normalization_trims_and_preserves_utf8() -> None:
    assert normalize_player_name("  María  ") == "María"


@pytest.mark.parametrize("value", ["", "   ", "A,B", "A\nB", "A\rB"])
def test_name_normalization_rejects_invalid_score_names(value: str) -> None:
    with pytest.raises(ValueError):
        normalize_player_name(value)


def test_name_normalization_enforces_public_length_limit() -> None:
    with pytest.raises(ValueError):
        normalize_player_name("X" * 21)


def test_name_entry_result_has_no_storage_side_effect_contract() -> None:
    assert NameEntryResult(name="PLAYER_01") == NameEntryResult("PLAYER_01", False)


def test_null_audio_service_supports_full_semantic_contract() -> None:
    audio = NullAudioService()
    assert audio.play_menu_music() is None
    assert audio.play_gameplay_music() is None
    assert audio.play_enemy_destroyed() is None
    assert audio.play_new_record() is None
    assert audio.stop_music() is None
