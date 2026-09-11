# -*- mode: python ; coding: utf-8 -*-
"""Controlled one-file Windows packaging profile for Vector Barrage.

This spec deliberately keeps project data minimal, uses the dedicated absolute-
import launcher, overrides Pygame's default PyInstaller hook, and removes the
known redistribution blockers from the analyzed archive.
"""

from pathlib import Path


SPEC_DIR = Path(SPEC).resolve().parent
PROJECT_ROOT = SPEC_DIR.parent
SRC_DIR = PROJECT_ROOT / "src"
LAUNCHER = SPEC_DIR / "vector_barrage_launcher.py"
SCORE_SEED = PROJECT_ROOT / "scores.txt"
HOOKS_DIR = SPEC_DIR / "hooks"

FORBIDDEN_DATA_BASENAMES = {
    "freesansbold.ttf",
    "pygame_icon.bmp",
    "pygame_icon_mac.bmp",
}
FORBIDDEN_BINARY_BASENAMES = {
    "vcruntime140.dll",
    "vcruntime140_1.dll",
}


def _toc_basenames(entry):
    """Return normalized basenames represented by one PyInstaller TOC entry."""

    values = [entry[0]]
    if len(entry) > 1:
        values.append(entry[1])
    return {Path(str(value)).name.lower() for value in values}


def _without_basenames(entries, forbidden):
    """Remove TOC entries whose destination/source basename is forbidden."""

    return [
        entry
        for entry in entries
        if _toc_basenames(entry).isdisjoint(forbidden)
    ]


a = Analysis(
    [str(LAUNCHER)],
    pathex=[str(SRC_DIR)],
    binaries=[],
    datas=[(str(SCORE_SEED), ".")],
    hiddenimports=[],
    hookspath=[str(HOOKS_DIR)],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

# Defense in depth: the local Pygame hook omits its default font/icon data, and
# the spec removes them again if any later hook or analysis step reintroduces
# them. The Microsoft VC runtime DLLs are intentionally external prerequisites.
a.datas = _without_basenames(a.datas, FORBIDDEN_DATA_BASENAMES)
a.binaries = _without_basenames(a.binaries, FORBIDDEN_BINARY_BASENAMES)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="VectorBarrage",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
