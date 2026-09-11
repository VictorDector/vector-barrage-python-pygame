"""High-score presentation screen for Vector Barrage."""

from __future__ import annotations

from enum import Enum, auto
from pathlib import Path

from ..storage import ScoreRecord, top_scores
from ..ui_fonts import create_system_font


class ScoresOutcome(Enum):
    RETURN_TO_MENU = auto()
    QUIT = auto()


def format_score_rows(records: list[ScoreRecord] | tuple[ScoreRecord, ...]) -> list[str]:
    """Format score records for presentation without filesystem or Pygame access."""

    return [
        f"{index:>2}. {record.name:<20} {record.score:>6}"
        for index, record in enumerate(records, start=1)
    ]


class ScoresScreen:
    """Display the current Top 5 and return control to the coordinator."""

    BACKGROUND = (7, 11, 24)
    TEXT = (226, 235, 247)
    ACCENT = (86, 220, 255)
    MUTED = (142, 157, 178)

    def __init__(self, score_path: Path) -> None:
        self.score_path = Path(score_path)

    def run(self, surface) -> ScoresOutcome:
        import pygame

        if not pygame.font.get_init():
            pygame.font.init()
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return ScoresOutcome.QUIT
                if event.type == pygame.KEYDOWN and event.key in {
                    pygame.K_ESCAPE,
                    pygame.K_BACKSPACE,
                    pygame.K_RETURN,
                    pygame.K_KP_ENTER,
                }:
                    return ScoresOutcome.RETURN_TO_MENU

            self.draw(surface)
            if pygame.display.get_surface() is surface:
                pygame.display.flip()
            clock.tick(60)

    def draw(self, surface) -> None:
        import pygame

        if not pygame.font.get_init():
            pygame.font.init()

        surface.fill(self.BACKGROUND)
        width, height = surface.get_size()
        title_font = create_system_font(58)
        score_font = create_system_font(34)
        hint_font = create_system_font(24)

        title = title_font.render("PUNTAJES", True, self.ACCENT)
        surface.blit(title, title.get_rect(center=(width // 2, 95)))

        rows = format_score_rows(top_scores(self.score_path))
        if rows:
            for index, row in enumerate(rows):
                text = score_font.render(row, True, self.TEXT)
                surface.blit(text, text.get_rect(center=(width // 2, 190 + index * 52)))
        else:
            empty = score_font.render("Aún no hay puntajes válidos.", True, self.MUTED)
            surface.blit(empty, empty.get_rect(center=(width // 2, height // 2)))

        hint = hint_font.render("ESC / ENTER: volver", True, self.MUTED)
        surface.blit(hint, hint.get_rect(center=(width // 2, height - 42)))
