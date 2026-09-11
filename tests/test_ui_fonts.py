"""Contract tests for the host-system font boundary."""

from __future__ import annotations

from pathlib import Path

import pytest

from vector_barrage.ui_fonts import resolve_system_font_path, system_font_candidates


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RUNTIME_FONT_SURFACES = (
    "src/vector_barrage/gameplay/renderer.py",
    "src/vector_barrage/screens/menu.py",
    "src/vector_barrage/screens/scores.py",
    "src/vector_barrage/screens/about.py",
    "src/vector_barrage/screens/name_entry.py",
)


def test_windows_candidates_prioritize_segoe_ui() -> None:
    candidates = system_font_candidates("Windows")
    assert candidates[0] == "segoeui"
    assert "arial" in candidates


def test_linux_candidates_include_common_system_sans_fonts() -> None:
    candidates = system_font_candidates("Linux")
    assert candidates[0] == "dejavusans"
    assert "liberationsans" in candidates


def test_resolver_returns_first_available_system_font_path() -> None:
    observed: list[str] = []

    def fake_match_font(name: str) -> str | None:
        observed.append(name)
        if name == "arial":
            return r"C:\Windows\Fonts\arial.ttf"
        return None

    path = resolve_system_font_path(
        platform_name="Windows",
        match_font=fake_match_font,
    )

    assert path == r"C:\Windows\Fonts\arial.ttf"
    assert observed == ["segoeui", "arial"]


def test_resolver_fails_closed_instead_of_using_pygame_default_font() -> None:
    with pytest.raises(RuntimeError, match="installed system sans-serif font"):
        resolve_system_font_path(
            platform_name="Windows",
            match_font=lambda _name: None,
        )


@pytest.mark.parametrize("relative_path", RUNTIME_FONT_SURFACES)
def test_runtime_text_surfaces_do_not_request_pygame_default_font(
    relative_path: str,
) -> None:
    source = (PROJECT_ROOT / relative_path).read_text(encoding="utf-8")
    assert "pygame.font.Font(None" not in source
    assert "create_system_font" in source
