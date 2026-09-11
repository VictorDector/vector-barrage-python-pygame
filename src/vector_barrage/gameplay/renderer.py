"""Primitive public renderer for Vector Barrage.

The renderer uses only programmatically generated geometry and host-system
fonts. No historical or third-party game artwork is required by this module.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..ui_fonts import create_system_font
from .model import GameState

if TYPE_CHECKING:
    import pygame


class GameRenderer:
    """Render the gameplay state using original geometric primitives."""

    BACKGROUND = (8, 12, 24)
    GRID = (18, 28, 48)
    PLAYER = (70, 210, 255)
    PLAYER_ACCENT = (210, 250, 255)
    ENEMY = (255, 100, 120)
    ENEMY_ACCENT = (255, 200, 110)
    PROJECTILE = (245, 245, 180)
    TEXT = (230, 238, 250)
    DANGER = (255, 90, 90)

    def draw(self, surface: "pygame.Surface", state: GameState) -> None:
        """Render one complete frame from authoritative gameplay state."""

        import pygame

        if not pygame.font.get_init():
            pygame.font.init()

        width, height = surface.get_size()
        surface.fill(self.BACKGROUND)

        for x in range(0, width, 80):
            pygame.draw.line(surface, self.GRID, (x, 0), (x, height), 1)
        for y in range(0, height, 80):
            pygame.draw.line(surface, self.GRID, (0, y), (width, y), 1)

        self._draw_player(surface, state)
        self._draw_enemies(surface, state)
        self._draw_projectiles(surface, state)
        self._draw_hud(surface, state)

        if state.game_over:
            self._draw_game_over(surface, state)

    def _draw_player(self, surface: "pygame.Surface", state: GameState) -> None:
        import pygame

        rect = state.player.rect
        left = int(rect.x)
        top = int(rect.y)
        right = int(rect.x + rect.width)
        bottom = int(rect.y + rect.height)
        center_x = int(rect.x + rect.width / 2)

        pygame.draw.polygon(
            surface,
            self.PLAYER,
            [(center_x, top), (right, bottom), (left, bottom)],
        )
        pygame.draw.line(
            surface,
            self.PLAYER_ACCENT,
            (center_x, top + 4),
            (center_x, bottom - 3),
            2,
        )

    def _draw_enemies(self, surface: "pygame.Surface", state: GameState) -> None:
        import pygame

        for enemy in state.enemies:
            if not enemy.alive:
                continue
            rect = pygame.Rect(
                round(enemy.rect.x),
                round(enemy.rect.y),
                round(enemy.rect.width),
                round(enemy.rect.height),
            )
            pygame.draw.rect(surface, self.ENEMY, rect, border_radius=5)
            inset = rect.inflate(-10, -10)
            if inset.width > 0 and inset.height > 0:
                pygame.draw.rect(surface, self.ENEMY_ACCENT, inset, 2, border_radius=3)

    def _draw_projectiles(self, surface: "pygame.Surface", state: GameState) -> None:
        import pygame

        for projectile in state.projectiles:
            if not projectile.active:
                continue
            rect = pygame.Rect(
                round(projectile.rect.x),
                round(projectile.rect.y),
                max(round(projectile.rect.width), 2),
                max(round(projectile.rect.height), 2),
            )
            pygame.draw.rect(surface, self.PROJECTILE, rect, border_radius=2)

    def _draw_hud(self, surface: "pygame.Surface", state: GameState) -> None:
        font = create_system_font(28)
        left = font.render(f"Vidas: {state.player.lives}", True, self.TEXT)
        center = font.render(f"Puntos: {state.score}", True, self.TEXT)
        right = font.render(f"Nivel: {state.level}", True, self.TEXT)

        surface.blit(left, (16, 14))
        surface.blit(center, ((surface.get_width() - center.get_width()) // 2, 14))
        surface.blit(right, (surface.get_width() - right.get_width() - 16, 14))

    def _draw_game_over(self, surface: "pygame.Surface", state: GameState) -> None:
        import pygame

        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        surface.blit(overlay, (0, 0))

        title_font = create_system_font(64)
        body_font = create_system_font(30)
        title = title_font.render("FIN DE PARTIDA", True, self.DANGER)
        score = body_font.render(f"Puntuación final: {state.score}", True, self.TEXT)
        prompt = body_font.render("ENTER: continuar · ESC: menú", True, self.TEXT)

        cx = surface.get_width() // 2
        cy = surface.get_height() // 2
        surface.blit(title, title.get_rect(center=(cx, cy - 50)))
        surface.blit(score, score.get_rect(center=(cx, cy + 10)))
        surface.blit(prompt, prompt.get_rect(center=(cx, cy + 50)))
