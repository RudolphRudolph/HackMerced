"""Core rarity types, kept apart from config.py so the config can import them."""

from dataclasses import dataclass
from enum import Enum


class Rarity(Enum):
    """Pack rarity tiers, from most common to rarest. Definition order is the tier order."""

    GREEN = "green"
    BLUE = "blue"
    YELLOW = "yellow"
    GOLD = "gold"
    RED = "red"


@dataclass(frozen=True)
class QualityTags:
    """Animagine quality tags added to the image prompt for one rarity."""

    positive: str
    negative: str
