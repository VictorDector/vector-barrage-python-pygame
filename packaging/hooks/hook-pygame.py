"""Project-local PyInstaller hook for Pygame in Vector Barrage.

The upstream Pygame hook adds the bundled default font and Pygame icon data.
Vector Barrage renders text from host-system fonts and does not require those
assets, so this hook retains Pygame's dynamic libraries while intentionally
collecting no Pygame data files.
"""

from PyInstaller.utils.hooks import collect_dynamic_libs


binaries = collect_dynamic_libs("pygame")
datas = []
