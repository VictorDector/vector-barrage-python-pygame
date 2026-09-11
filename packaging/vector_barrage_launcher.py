"""Thin native-packaging launcher for Vector Barrage.

This module exists only to provide PyInstaller with an absolute package import
boundary. Normal source execution remains ``python -m vector_barrage``.
"""

from vector_barrage.app import main


if __name__ == "__main__":
    main()
