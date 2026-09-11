"""Contract tests for clean read-only resource resolution."""

from __future__ import annotations

from pathlib import Path
import sys

import pytest

from vector_barrage.resources import read_only_resource_root, require_resource, resource_paths


def test_resource_paths_use_clean_assets_tree() -> None:
    paths = resource_paths()
    assert paths.images == paths.root / "assets" / "images"
    assert paths.audio == paths.root / "assets" / "audio"


def test_pyinstaller_bundle_root_takes_precedence(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setattr(sys, "_MEIPASS", str(tmp_path), raising=False)
    assert read_only_resource_root() == tmp_path


def test_require_resource_rejects_missing_and_accepts_file(tmp_path: Path) -> None:
    path = tmp_path / "asset.dat"
    with pytest.raises(FileNotFoundError):
        require_resource(path)
    path.write_bytes(b"clean")
    assert require_resource(path) == path
