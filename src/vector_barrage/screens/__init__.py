"""User-interface screens for Vector Barrage.

Screens own only their local interaction loop and return outcomes to the
application coordinator. They do not create or invoke other screens.
"""

from .about import AboutOutcome, AboutScreen
from .menu import MainMenuScreen, MenuChoice
from .name_entry import NameEntryResult, NameEntryScreen
from .scores import ScoresOutcome, ScoresScreen

__all__ = [
    "AboutOutcome",
    "AboutScreen",
    "MainMenuScreen",
    "MenuChoice",
    "NameEntryResult",
    "NameEntryScreen",
    "ScoresOutcome",
    "ScoresScreen",
]
