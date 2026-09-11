# Notice

Project: **Vector Barrage**  
Release target: `v1.1.0`

## Purpose

This notice records authorship, provenance and the third-party software boundary for the public, source-first Vector Barrage portfolio repository. It is not a substitute for the repository `LICENSE` or for the licenses that govern third-party software.

## Project Authorship

Vector Barrage is an independently implemented Python/Pygame desktop game authored and integrated by:

**Victor David Dector Ramirez**

Vector Barrage-owned source code, tests, engineering documentation, procedural presentation logic and synthetic score seed are released under the repository MIT `LICENSE`, subject to the third-party boundary below.

## Third-Party Software

Vector Barrage requires Python 3.13.x and declares `pygame==2.6.1` as its runtime dependency. Development/build tooling also includes setuptools, pytest and PyInstaller as declared in `pyproject.toml`.

These projects are not relicensed by the Vector Barrage MIT license. Each remains governed by its own license, copyright notices and terms.

Under the current publication profile:

```text
PUBLIC SOURCE REPOSITORY      = YES
PYTHON/PYGAME DEPENDENCIES    = INSTALLED BY THE USER
PUBLIC EXECUTABLE DOWNLOAD    = NO
BUNDLED THIRD-PARTY BINARIES  = NO
```

The repository provides source code and reproducible setup/run instructions. It does not currently distribute `VectorBarrage.exe` or another bundled executable containing Python/Pygame runtime components.

If public executable distribution is introduced later, binary-specific third-party license and redistribution requirements must be reactivated and completed before that artifact is released.

## Visual and Audio Material

The current candidate does not require copied gameplay artwork, sprite files, music tracks, sound-effect files or bundled font files. Visuals are generated using Pygame drawing primitives and host-system font rendering. Audio is generated procedurally from source-defined tone data.

## Learning / Provenance Context

The broader development effort was informed by academic Pygame learning materials and general software-development references. Those materials are learning/provenance context only. The public Vector Barrage repository does not claim ownership of third-party instructional source expression, course assets, trademarks or branding.

## Public Data

The repository default `scores.txt` uses synthetic `PLAYER_XX` identifiers and is intended only as demonstration/seed data.

## Trademarks

Third-party names and trademarks referenced for factual technical identification remain the property of their respective owners. No affiliation, sponsorship or endorsement is implied.

## Current Licensing Boundary

```text
VECTOR BARRAGE-OWNED MATERIAL = MIT
PYGAME                        = THIRD-PARTY / OWN LICENSE
PYTHON                        = THIRD-PARTY / OWN LICENSE
OTHER TOOLING                 = THIRD-PARTY / OWN LICENSES
PUBLIC WINDOWS BINARY         = NOT DISTRIBUTED
```

See `LICENSE` for the rights granted for Vector Barrage-owned material and `pyproject.toml` for the declared runtime/development dependency boundary.
