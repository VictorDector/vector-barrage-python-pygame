"""Pygame runtime/session orchestration for Vector Barrage.

The helper functions in this module are deterministic and Pygame-independent.
The ``GameSession.run`` method owns Pygame event processing and rendering.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, replace
from enum import Enum, auto

from .model import (
    DEFAULT_GAMEPLAY_CONFIG,
    EnemyState,
    GameState,
    GameplayConfig,
    PlayerState,
    ProjectileState,
    Rect,
)
from .rules import (
    add_projectile,
    advance_level_if_cleared,
    apply_player_damage,
    move_player_horizontally,
    resolve_projectile_enemy_collisions,
)


@dataclass(frozen=True, slots=True)
class SessionTuning:
    player_width: float = 48.0
    player_height: float = 24.0
    player_bottom_margin: float = 36.0
    player_speed: float = 360.0
    projectile_width: float = 4.0
    projectile_height: float = 14.0
    projectile_speed: float = 520.0
    enemy_width: float = 36.0
    enemy_height: float = 24.0
    enemy_columns: int = 8
    enemy_rows: int = 3
    enemy_gap_x: float = 18.0
    enemy_gap_y: float = 16.0
    enemy_top_margin: float = 72.0
    enemy_speed: float = 72.0
    enemy_drop: float = 18.0
    fire_cooldown_ms: int = 180


DEFAULT_SESSION_TUNING = SessionTuning()


class SessionOutcome(Enum):
    RETURN_TO_MENU = auto()
    QUIT = auto()


@dataclass(frozen=True, slots=True)
class GameSessionResult:
    final_score: int
    outcome: SessionOutcome
    completed: bool = False


@dataclass(frozen=True, slots=True)
class EnemyMotion:
    enemies: tuple[EnemyState, ...]
    direction: int
    breached: bool = False


def create_enemy_wave(
    level: int,
    *,
    config: GameplayConfig = DEFAULT_GAMEPLAY_CONFIG,
    tuning: SessionTuning = DEFAULT_SESSION_TUNING,
) -> tuple[EnemyState, ...]:
    """Create one deterministic centered enemy formation."""

    if level < 1:
        raise ValueError("level must be at least 1")
    if tuning.enemy_columns < 1 or tuning.enemy_rows < 1:
        raise ValueError("enemy rows and columns must be positive")

    formation_width = (
        tuning.enemy_columns * tuning.enemy_width
        + (tuning.enemy_columns - 1) * tuning.enemy_gap_x
    )
    start_x = max((config.playfield_width - formation_width) / 2.0, 0.0)
    enemies: list[EnemyState] = []
    enemy_id = 1

    for row in range(tuning.enemy_rows):
        for column in range(tuning.enemy_columns):
            x = start_x + column * (tuning.enemy_width + tuning.enemy_gap_x)
            y = tuning.enemy_top_margin + row * (tuning.enemy_height + tuning.enemy_gap_y)
            enemies.append(
                EnemyState(
                    enemy_id=enemy_id,
                    rect=Rect(x, y, tuning.enemy_width, tuning.enemy_height),
                )
            )
            enemy_id += 1

    return tuple(enemies)


def create_initial_state(
    *,
    config: GameplayConfig = DEFAULT_GAMEPLAY_CONFIG,
    tuning: SessionTuning = DEFAULT_SESSION_TUNING,
) -> GameState:
    """Create a fresh gameplay state for a new session."""

    player_x = (config.playfield_width - tuning.player_width) / 2.0
    player_y = config.playfield_height - tuning.player_bottom_margin - tuning.player_height
    return GameState(
        player=PlayerState(
            Rect(player_x, player_y, tuning.player_width, tuning.player_height),
            lives=config.starting_lives,
        ),
        enemies=create_enemy_wave(1, config=config, tuning=tuning),
    )


def create_player_projectile(
    state: GameState,
    projectile_id: int,
    *,
    tuning: SessionTuning = DEFAULT_SESSION_TUNING,
) -> ProjectileState:
    """Create a projectile centered above the current player."""

    if projectile_id < 1:
        raise ValueError("projectile_id must be positive")

    x = state.player.rect.x + (state.player.rect.width - tuning.projectile_width) / 2.0
    y = state.player.rect.y - tuning.projectile_height
    return ProjectileState(
        projectile_id=projectile_id,
        rect=Rect(x, y, tuning.projectile_width, tuning.projectile_height),
    )


def move_active_projectiles(
    state: GameState,
    elapsed_seconds: float,
    *,
    tuning: SessionTuning = DEFAULT_SESSION_TUNING,
) -> GameState:
    """Advance active player projectiles upward and discard expired ones."""

    if elapsed_seconds < 0:
        raise ValueError("elapsed_seconds must be non-negative")

    moved: list[ProjectileState] = []
    delta_y = -tuning.projectile_speed * elapsed_seconds
    for projectile in state.projectiles:
        if not projectile.active:
            continue
        rect = projectile.rect.moved(dy=delta_y)
        if rect.y + rect.height <= 0:
            continue
        moved.append(replace(projectile, rect=rect))
    return replace(state, projectiles=tuple(moved))


def move_enemy_formation(
    enemies: tuple[EnemyState, ...],
    direction: int,
    elapsed_seconds: float,
    *,
    level: int = 1,
    config: GameplayConfig = DEFAULT_GAMEPLAY_CONFIG,
    tuning: SessionTuning = DEFAULT_SESSION_TUNING,
    breach_y: float | None = None,
) -> EnemyMotion:
    """Move the living formation horizontally, reversing and dropping at edges."""

    if direction not in {-1, 1}:
        raise ValueError("direction must be -1 or 1")
    if elapsed_seconds < 0:
        raise ValueError("elapsed_seconds must be non-negative")
    if level < 1:
        raise ValueError("level must be at least 1")

    living = [enemy for enemy in enemies if enemy.alive]
    if not living:
        return EnemyMotion(enemies=enemies, direction=direction)

    speed = tuning.enemy_speed * (1.0 + 0.12 * (level - 1))
    dx = direction * speed * elapsed_seconds
    left = min(enemy.rect.x for enemy in living)
    right = max(enemy.rect.x + enemy.rect.width for enemy in living)
    hit_edge = left + dx < 0.0 or right + dx > config.playfield_width

    next_direction = -direction if hit_edge else direction
    effective_dx = 0.0 if hit_edge else dx
    drop = tuning.enemy_drop if hit_edge else 0.0

    moved: list[EnemyState] = []
    for enemy in enemies:
        if not enemy.alive:
            moved.append(enemy)
            continue
        moved.append(
            replace(
                enemy,
                rect=enemy.rect.moved(dx=effective_dx, dy=drop),
            )
        )

    threshold = config.playfield_height if breach_y is None else breach_y
    breached = any(
        enemy.alive and enemy.rect.y + enemy.rect.height >= threshold
        for enemy in moved
    )
    return EnemyMotion(tuple(moved), next_direction, breached)


def advance_runtime_state(
    state: GameState,
    elapsed_seconds: float,
    *,
    enemy_direction: int,
    config: GameplayConfig = DEFAULT_GAMEPLAY_CONFIG,
    tuning: SessionTuning = DEFAULT_SESSION_TUNING,
) -> tuple[GameState, int, tuple[int, ...]]:
    """Advance one deterministic simulation step outside of direct input handling."""

    if state.game_over:
        return state, enemy_direction, ()

    state = move_active_projectiles(state, elapsed_seconds, tuning=tuning)
    motion = move_enemy_formation(
        state.enemies,
        enemy_direction,
        elapsed_seconds,
        level=state.level,
        config=config,
        tuning=tuning,
        breach_y=state.player.rect.y,
    )
    state = replace(state, enemies=motion.enemies)
    state, destroyed_ids = resolve_projectile_enemy_collisions(state, config=config)
    surviving_breach = any(
        enemy.alive and enemy.rect.y + enemy.rect.height >= state.player.rect.y
        for enemy in state.enemies
    )

    if surviving_breach and not state.game_over:
        state = apply_player_damage(state)
        if not state.game_over:
            state = replace(
                state,
                enemies=create_enemy_wave(state.level, config=config, tuning=tuning),
                projectiles=(),
            )
        return state, 1, destroyed_ids

    advanced = advance_level_if_cleared(state)
    if advanced.level != state.level:
        advanced = replace(
            advanced,
            enemies=create_enemy_wave(advanced.level, config=config, tuning=tuning),
            projectiles=(),
        )
        return advanced, 1, destroyed_ids

    return state, motion.direction, destroyed_ids


class GameSession:
    """Own the Pygame gameplay loop and adapt input/rendering to domain rules."""

    def __init__(
        self,
        *,
        config: GameplayConfig = DEFAULT_GAMEPLAY_CONFIG,
        tuning: SessionTuning = DEFAULT_SESSION_TUNING,
    ) -> None:
        self.config = config
        self.tuning = tuning

    def run(
        self,
        surface=None,
        *,
        on_enemy_destroyed: Callable[[int], None] | None = None,
    ) -> GameSessionResult:
        """Run a graphical gameplay session and return its final outcome."""

        import pygame

        from .renderer import GameRenderer

        own_display = surface is None
        if own_display:
            if not pygame.get_init():
                pygame.init()
            surface = pygame.display.set_mode(
                (int(self.config.playfield_width), int(self.config.playfield_height))
            )
            pygame.display.set_caption("Vector Barrage")

        renderer = GameRenderer()
        clock = pygame.time.Clock()
        state = create_initial_state(config=self.config, tuning=self.tuning)
        enemy_direction = 1
        next_projectile_id = 1
        last_fire_ms = -self.tuning.fire_cooldown_ms

        while True:
            elapsed_seconds = min(clock.tick(60) / 1000.0, 0.05)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return GameSessionResult(state.score, SessionOutcome.QUIT)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return GameSessionResult(
                            state.score,
                            SessionOutcome.RETURN_TO_MENU,
                            completed=False,
                        )
                    if (
                        event.key == pygame.K_SPACE
                        and not state.game_over
                        and pygame.time.get_ticks() - last_fire_ms >= self.tuning.fire_cooldown_ms
                    ):
                        state = add_projectile(
                            state,
                            create_player_projectile(
                                state,
                                next_projectile_id,
                                tuning=self.tuning,
                            ),
                        )
                        next_projectile_id += 1
                        last_fire_ms = pygame.time.get_ticks()
                    if state.game_over and event.key in {pygame.K_RETURN, pygame.K_KP_ENTER}:
                        return GameSessionResult(
                            state.score,
                            SessionOutcome.RETURN_TO_MENU,
                            completed=True,
                        )

            if not state.game_over:
                keys = pygame.key.get_pressed()
                direction = float(keys[pygame.K_RIGHT] - keys[pygame.K_LEFT])
                if direction:
                    player = move_player_horizontally(
                        state.player,
                        direction * self.tuning.player_speed * elapsed_seconds,
                        playfield_width=self.config.playfield_width,
                    )
                    state = replace(state, player=player)

                state, enemy_direction, destroyed_ids = advance_runtime_state(
                    state,
                    elapsed_seconds,
                    enemy_direction=enemy_direction,
                    config=self.config,
                    tuning=self.tuning,
                )
                if on_enemy_destroyed is not None:
                    for enemy_id in destroyed_ids:
                        on_enemy_destroyed(enemy_id)

            renderer.draw(surface, state)
            if pygame.display.get_surface() is surface:
                pygame.display.flip()

            if own_display and not pygame.display.get_init():
                return GameSessionResult(state.score, SessionOutcome.QUIT)
