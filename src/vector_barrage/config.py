"""Stable public configuration values for Vector Barrage."""

from dataclasses import dataclass

PRODUCT_NAME = "Vector Barrage"
PUBLIC_GITHUB_URL = "https://github.com/VictorDector/vector-barrage-python-pygame"
AUTHOR_NAME = "Victor David Dector Ramirez"


@dataclass(frozen=True, slots=True)
class AppConfig:
    """Application-level settings that do not belong to gameplay state."""

    window_width: int = 800
    window_height: int = 600
    target_fps: int = 60
    interface_language: str = "es"


DEFAULT_CONFIG = AppConfig()
