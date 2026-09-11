"""Static contract tests for the controlled PyInstaller packaging profile."""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SPEC_PATH = PROJECT_ROOT / "packaging" / "VectorBarrage.spec"
HOOK_PATH = PROJECT_ROOT / "packaging" / "hooks" / "hook-pygame.py"
GITIGNORE_PATH = PROJECT_ROOT / ".gitignore"


def test_controlled_spec_is_explicitly_source_tracked() -> None:
    gitignore = GITIGNORE_PATH.read_text(encoding="utf-8")
    assert "*.spec" in gitignore
    assert "!packaging/VectorBarrage.spec" in gitignore


def test_controlled_spec_has_valid_python_syntax() -> None:
    spec = SPEC_PATH.read_text(encoding="utf-8")
    compile(spec, str(SPEC_PATH), "exec")


def test_spec_uses_launcher_src_seed_and_custom_hook_directory() -> None:
    spec = SPEC_PATH.read_text(encoding="utf-8")
    assert 'LAUNCHER = SPEC_DIR / "vector_barrage_launcher.py"' in spec
    assert 'SRC_DIR = PROJECT_ROOT / "src"' in spec
    assert 'SCORE_SEED = PROJECT_ROOT / "scores.txt"' in spec
    assert 'HOOKS_DIR = SPEC_DIR / "hooks"' in spec
    assert "hookspath=[str(HOOKS_DIR)]" in spec


def test_spec_defensively_excludes_pygame_default_data_assets() -> None:
    spec = SPEC_PATH.read_text(encoding="utf-8").lower()
    assert '"freesansbold.ttf"' in spec
    assert '"pygame_icon.bmp"' in spec
    assert "a.datas = _without_basenames" in spec


def test_spec_excludes_msvc_runtime_dlls_from_bundle() -> None:
    spec = SPEC_PATH.read_text(encoding="utf-8").lower()
    assert '"vcruntime140.dll"' in spec
    assert '"vcruntime140_1.dll"' in spec
    assert "a.binaries = _without_basenames" in spec


def test_local_pygame_hook_keeps_dynamic_libraries_but_collects_no_data() -> None:
    hook = HOOK_PATH.read_text(encoding="utf-8")
    assert 'binaries = collect_dynamic_libs("pygame")' in hook
    assert "datas = []" in hook
    assert "collect_data_files(" not in hook
    assert "_append_to_datas(" not in hook


def test_spec_preserves_onefile_windowed_executable_profile() -> None:
    spec = SPEC_PATH.read_text(encoding="utf-8")
    assert "exe = EXE(" in spec
    assert 'name="VectorBarrage"' in spec
    assert "console=False" in spec
    assert "COLLECT(" not in spec
