"""Programmatic Main Menu screen for Vector Barrage."""

from __future__ import annotations

from enum import Enum, auto

from ..ui_fonts import create_system_font


class MenuChoice(Enum):
    GAME = auto()
    SCORES = auto()
    ABOUT = auto()
    EXIT = auto()


MENU_CHOICES = (
    ("Jugar", MenuChoice.GAME),
    ("Puntajes", MenuChoice.SCORES),
    ("Acerca de", MenuChoice.ABOUT),
    ("Salir", MenuChoice.EXIT),
)


def menu_choice_for_index(index: int) -> MenuChoice:
    """Resolve one visible menu index to a coordinator-facing choice."""

    try:
        return MENU_CHOICES[index][1]
    except IndexError as exc:
        raise ValueError(f"invalid menu index: {index}") from exc


class MainMenuScreen:
    """Own one Main Menu interaction lifecycle and return one selection."""

    BACKGROUND = (7, 11, 24)
    TEXT = (224, 235, 248)
    SELECTED = (86, 220, 255)
    MUTED = (128, 145, 166)

    def __init__(self, *, title: str = "Vector Barrage") -> None:
        self.title = title

    def run(self, surface) -> MenuChoice:
        import pygame

        if not pygame.font.get_init():
            pygame.font.init()

        clock = pygame.time.Clock()
        selected = 0

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return MenuChoice.EXIT
                if event.type == pygame.KEYDOWN:
                    if event.key in {pygame.K_UP, pygame.K_w}:
                        selected = (selected - 1) % len(MENU_CHOICES)
                    elif event.key in {pygame.K_DOWN, pygame.K_s}:
                        selected = (selected + 1) % len(MENU_CHOICES)
                    elif event.key in {pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE}:
                        return menu_choice_for_index(selected)
                    elif event.key == pygame.K_ESCAPE:
                        return MenuChoice.EXIT

            self.draw(surface, selected)
            if pygame.display.get_surface() is surface:
                pygame.display.flip()
            clock.tick(60)

    def draw(self, surface, selected: int = 0) -> None:
        import pygame

        if not 0 <= selected < len(MENU_CHOICES):
            raise ValueError("selected menu index out of range")
        if not pygame.font.get_init():
            pygame.font.init()

        surface.fill(self.BACKGROUND)
        width, height = surface.get_size()

        for x in range(0, width, 64):
            pygame.draw.line(surface, (15, 24, 46), (x, 0), (x, height), 1)
        for y in range(0, height, 64):
            pygame.draw.line(surface, (15, 24, 46), (0, y), (width, y), 1)

        title_font = create_system_font(72)
        option_font = create_system_font(40)
        hint_font = create_system_font(24)

        title = title_font.render(self.title, True, self.TEXT)
        surface.blit(title, title.get_rect(center=(width // 2, 120)))

        start_y = 240
        for index, (label, _) in enumerate(MENU_CHOICES):
            color = self.SELECTED if index == selected else self.TEXT
            text = option_font.render(label, True, color)
            surface.blit(text, text.get_rect(center=(width // 2, start_y + index * 58)))

        hint = hint_font.render("↑/↓ seleccionar · ENTER confirmar", True, self.MUTED)
        surface.blit(hint, hint.get_rect(center=(width // 2, height - 42)))
