"""Controlled new-record name entry for Vector Barrage."""

from __future__ import annotations

from dataclasses import dataclass

from ..ui_fonts import create_system_font


MAX_PLAYER_NAME_LENGTH = 20


@dataclass(frozen=True, slots=True)
class NameEntryResult:
    """Outcome returned to the application coordinator/integration boundary."""

    name: str | None = None
    quit_requested: bool = False


def normalize_player_name(
    value: str,
    *,
    max_length: int = MAX_PLAYER_NAME_LENGTH,
) -> str:
    """Validate and normalize one public score name."""

    if max_length < 1:
        raise ValueError("max_length must be positive")

    name = value.strip()
    if not name:
        raise ValueError("name must not be empty or whitespace-only")
    if "," in name or "\n" in name or "\r" in name:
        raise ValueError("name must not contain commas or line breaks")
    if len(name) > max_length:
        raise ValueError(f"name must contain at most {max_length} characters")
    return name


class NameEntryScreen:
    """Capture one validated name without writing score storage directly."""

    BACKGROUND = (7, 11, 24)
    TEXT = (226, 235, 247)
    ACCENT = (86, 220, 255)
    ERROR = (255, 110, 120)
    MUTED = (142, 157, 178)

    def __init__(self, final_score: int, *, max_length: int = MAX_PLAYER_NAME_LENGTH) -> None:
        if final_score < 0:
            raise ValueError("final_score must be non-negative")
        if max_length < 1:
            raise ValueError("max_length must be positive")
        self.final_score = final_score
        self.max_length = max_length

    def run(self, surface) -> NameEntryResult:
        import pygame

        if not pygame.font.get_init():
            pygame.font.init()

        clock = pygame.time.Clock()
        buffer = ""
        error_message = ""

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return NameEntryResult(quit_requested=True)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return NameEntryResult()
                    if event.key == pygame.K_BACKSPACE:
                        buffer = buffer[:-1]
                        error_message = ""
                    elif event.key in {pygame.K_RETURN, pygame.K_KP_ENTER}:
                        try:
                            normalized = normalize_player_name(
                                buffer,
                                max_length=self.max_length,
                            )
                        except ValueError as exc:
                            error_message = str(exc)
                        else:
                            return NameEntryResult(name=normalized)
                    elif event.unicode and event.unicode.isprintable():
                        if len(buffer) < self.max_length:
                            buffer += event.unicode
                            error_message = ""

            self.draw(surface, buffer, error_message)
            if pygame.display.get_surface() is surface:
                pygame.display.flip()
            clock.tick(60)

    def draw(self, surface, buffer: str, error_message: str = "") -> None:
        import pygame

        if not pygame.font.get_init():
            pygame.font.init()

        surface.fill(self.BACKGROUND)
        width, height = surface.get_size()

        title_font = create_system_font(54)
        body_font = create_system_font(30)
        input_font = create_system_font(38)
        hint_font = create_system_font(22)

        title = title_font.render("NUEVO RÉCORD", True, self.ACCENT)
        score = body_font.render(f"Puntuación: {self.final_score}", True, self.TEXT)
        prompt = body_font.render("Escribe tu nombre:", True, self.TEXT)

        surface.blit(title, title.get_rect(center=(width // 2, 120)))
        surface.blit(score, score.get_rect(center=(width // 2, 185)))
        surface.blit(prompt, prompt.get_rect(center=(width // 2, 245)))

        input_rect = pygame.Rect(width // 2 - 190, 285, 380, 54)
        pygame.draw.rect(surface, self.ACCENT, input_rect, 2, border_radius=6)
        rendered = input_font.render(buffer, True, self.TEXT)
        surface.blit(rendered, (input_rect.x + 12, input_rect.y + 10))

        if error_message:
            error = hint_font.render(error_message, True, self.ERROR)
            surface.blit(error, error.get_rect(center=(width // 2, 370)))

        hint = hint_font.render("ENTER: guardar · ESC: cancelar", True, self.MUTED)
        surface.blit(hint, hint.get_rect(center=(width // 2, height - 42)))
