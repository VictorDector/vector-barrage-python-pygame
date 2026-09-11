"""About screen for the clean public Vector Barrage implementation."""

from __future__ import annotations

from enum import Enum, auto

from ..config import AUTHOR_NAME, PRODUCT_NAME, PUBLIC_GITHUB_URL
from ..links import open_external_url
from ..ui_fonts import create_system_font


class AboutOutcome(Enum):
    RETURN_TO_MENU = auto()
    QUIT = auto()


def about_lines() -> tuple[str, ...]:
    """Return stable public About copy independently of Pygame."""

    return (
        PRODUCT_NAME,
        "Juego arcade de disparos fijos creado con Python y Pygame.",
        f"Autor: {AUTHOR_NAME}",
        "Implementación pública independiente con medios generados.",
    )


def wrap_text_to_width(text: str, font, max_width: int) -> tuple[str, ...]:
    """Wrap text on word boundaries so each rendered line fits ``max_width``."""

    if max_width <= 0:
        raise ValueError("max_width must be positive")

    words = text.split()
    if not words:
        return ("",)

    wrapped: list[str] = []
    current = words[0]

    for word in words[1:]:
        candidate = f"{current} {word}"
        if font.size(candidate)[0] <= max_width:
            current = candidate
        else:
            wrapped.append(current)
            current = word

    wrapped.append(current)
    return tuple(wrapped)


class AboutScreen:
    """Render public product information and expose the approved project link."""

    BACKGROUND = (7, 11, 24)
    TEXT = (226, 235, 247)
    ACCENT = (86, 220, 255)
    MUTED = (142, 157, 178)

    def __init__(self, *, github_url: str = PUBLIC_GITHUB_URL) -> None:
        self.github_url = github_url

    def run(self, surface) -> AboutOutcome:
        import pygame

        if not pygame.font.get_init():
            pygame.font.init()
        clock = pygame.time.Clock()

        while True:
            link_rect = self.draw(surface)
            if pygame.display.get_surface() is surface:
                pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return AboutOutcome.QUIT
                if event.type == pygame.KEYDOWN:
                    if event.key in {pygame.K_ESCAPE, pygame.K_BACKSPACE}:
                        return AboutOutcome.RETURN_TO_MENU
                    if event.key == pygame.K_g:
                        open_external_url(self.github_url)
                if (
                    event.type == pygame.MOUSEBUTTONUP
                    and event.button == 1
                    and link_rect.collidepoint(event.pos)
                ):
                    open_external_url(self.github_url)

            clock.tick(60)

    def draw(self, surface):
        import pygame

        if not pygame.font.get_init():
            pygame.font.init()

        surface.fill(self.BACKGROUND)
        width, height = surface.get_size()
        title_font = create_system_font(60)
        body_font = create_system_font(30)
        link_font = create_system_font(30)
        hint_font = create_system_font(23)

        lines = about_lines()
        title = title_font.render(lines[0], True, self.ACCENT)
        surface.blit(title, title.get_rect(center=(width // 2, 95)))

        body_max_width = max(width - 120, 1)
        body_y = 175
        line_step = max(body_font.get_linesize(), 34)
        paragraph_gap = 8

        for paragraph in lines[1:]:
            for wrapped_line in wrap_text_to_width(paragraph, body_font, body_max_width):
                text = body_font.render(wrapped_line, True, self.TEXT)
                surface.blit(text, text.get_rect(center=(width // 2, body_y)))
                body_y += line_step
            body_y += paragraph_gap

        link = link_font.render("GitHub del proyecto", True, self.ACCENT)
        link_y = min(max(390, body_y + 10), height - 110)
        link_rect = link.get_rect(center=(width // 2, link_y))
        surface.blit(link, link_rect)

        hint = hint_font.render("G / clic: abrir GitHub · ESC: volver", True, self.MUTED)
        surface.blit(hint, hint.get_rect(center=(width // 2, height - 42)))
        return link_rect
