"""External-link boundary for Vector Barrage."""

from __future__ import annotations

from collections.abc import Callable
import os
import shutil
import subprocess
from urllib.parse import urlparse
import webbrowser


def validate_public_url(url: str) -> str:
    """Return a normalized public HTTPS URL or raise ``ValueError``."""

    candidate = url.strip()
    parsed = urlparse(candidate)
    if parsed.scheme.lower() != "https" or not parsed.netloc:
        raise ValueError("public links must use an absolute HTTPS URL")
    if parsed.username or parsed.password:
        raise ValueError("public links must not contain embedded credentials")
    return candidate


def is_wsl() -> bool:
    """Return True when execution is inside Windows Subsystem for Linux."""

    return bool(os.environ.get("WSL_DISTRO_NAME"))


def open_external_url(
    url: str,
    *,
    browser_opener: Callable[[str], bool] | None = None,
) -> bool:
    """Open an approved URL through the platform boundary.

    WSL prefers ``explorer.exe`` when available. Other environments use
    ``webbrowser.open``. The URL is validated before any external process is
    invoked.
    """

    target = validate_public_url(url)

    if is_wsl() and shutil.which("explorer.exe"):
        try:
            completed = subprocess.run(
                ["explorer.exe", target],
                check=False,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except OSError:
            pass
        else:
            if completed.returncode == 0:
                return True

    opener = browser_opener or webbrowser.open
    return bool(opener(target))
