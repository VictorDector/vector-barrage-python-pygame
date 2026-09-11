"""System-hosted font resolution for Vector Barrage UI surfaces.

This module deliberately avoids Pygame's bundled default font. Public runtime
text is rendered from fonts already installed on the host operating system so
packaged builds do not need to redistribute ``pygame/freesansbold.ttf``.
"""

from __future__ import annotations

import platform
from collections.abc import Callable


_WINDOWS_FONT_CANDIDATES = ("segoeui", "arial", "tahoma")
_LINUX_FONT_CANDIDATES = ("dejavusans", "liberationsans", "ubuntu", "notosans")
_MACOS_FONT_CANDIDATES = ("helvetica", "arial")
_GENERIC_FONT_CANDIDATES = ("arial", "dejavusans", "liberationsans", "notosans")


def system_font_candidates(platform_name: str | None = None) -> tuple[str, ...]:
    """Return ordered system-font candidates for one host platform."""

    resolved = (platform_name or platform.system()).strip().lower()
    if resolved == "windows":
        return _WINDOWS_FONT_CANDIDATES
    if resolved == "linux":
        return _LINUX_FONT_CANDIDATES
    if resolved == "darwin":
        return _MACOS_FONT_CANDIDATES
    return _GENERIC_FONT_CANDIDATES


def resolve_system_font_path(
    *,
    platform_name: str | None = None,
    match_font: Callable[[str], str | None] | None = None,
) -> str:
    """Resolve the first available host font without default-font fallback."""

    if match_font is None:
        import pygame

        match_font = pygame.font.match_font

    for candidate in system_font_candidates(platform_name):
        path = match_font(candidate)
        if path:
            return path

    raise RuntimeError(
        "Vector Barrage requires an installed system sans-serif font; "
        "no approved host font candidate was found."
    )


def create_system_font(
    size: int,
    *,
    bold: bool = False,
    italic: bool = False,
    platform_name: str | None = None,
):
    """Create a Pygame Font from an explicit host-system font path."""

    if size < 1:
        raise ValueError("font size must be positive")

    import pygame

    if not pygame.font.get_init():
        pygame.font.init()

    def match_font(name: str) -> str | None:
        return pygame.font.match_font(name, bold=bold, italic=italic)

    path = resolve_system_font_path(
        platform_name=platform_name,
        match_font=match_font,
    )
    return pygame.font.Font(path, size)
