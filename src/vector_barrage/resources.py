"""Runtime resource-location helpers for Vector Barrage.

No historical assets are bundled by this module. It only defines clean paths for
future approved public media and PyInstaller read-only resources.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sys


@dataclass(frozen=True, slots=True)
class ResourcePaths:
    root: Path
    images: Path
    audio: Path


def source_project_root() -> Path:
    """Return the source checkout root for the ``src`` package layout."""

    return Path(__file__).resolve().parents[2]


def read_only_resource_root() -> Path:
    """Return the root for bundled read-only resources.

    PyInstaller exposes bundled read-only files under ``sys._MEIPASS``. Source
    execution resolves resources from the project root. Writable score data is
    deliberately not resolved here.
    """

    bundle_root = getattr(sys, "_MEIPASS", None)
    if bundle_root is not None:
        return Path(bundle_root)
    return source_project_root()


def resource_paths() -> ResourcePaths:
    """Return approved public media directories without creating them."""

    root = read_only_resource_root()
    assets = root / "assets"
    return ResourcePaths(
        root=root,
        images=assets / "images",
        audio=assets / "audio",
    )


def require_resource(path: Path) -> Path:
    """Return an existing resource path or raise a precise error."""

    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"Required Vector Barrage resource not found: {path}")
    return path
