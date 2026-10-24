"""Weighted rarity rolls. Pure logic: no web or image-generation code here."""

import math
import random
from collections.abc import Mapping

from app.config import DROP_WEIGHTS, QUALITY_TAGS
from app.models import QualityTags, Rarity

# Not cryptographic on purpose: the game runs locally, so tampering only affects that player.
_default_rng = random.Random()


class RarityConfigError(ValueError):
    """Raised when a drop-weight config can't be used for a roll."""


def validate_weights(weights: Mapping[Rarity, float]) -> None:
    """Raise RarityConfigError unless every tier has a finite weight >= 0 and the total is positive."""
    if not weights:
        raise RarityConfigError("Drop weights are empty. Give every Rarity tier a weight.")

    missing = [tier.name for tier in Rarity if tier not in weights]
    unknown = [repr(key) for key in weights if not isinstance(key, Rarity)]
    if missing or unknown:
        raise RarityConfigError(
            f"Drop weights must list exactly the Rarity tiers. Missing: {missing}. Unknown: {unknown}."
        )

    for tier, weight in weights.items():
        is_number = isinstance(weight, (int, float)) and not isinstance(weight, bool)
        if not is_number or not math.isfinite(weight) or weight < 0:
            raise RarityConfigError(f"Weight for {tier.name} must be a finite number >= 0, got {weight!r}.")

    if sum(weights.values()) <= 0:
        raise RarityConfigError("At least one drop weight must be greater than 0.")


def roll_rarity(
    rng: random.Random | None = None,
    weights: Mapping[Rarity, float] | None = None,
) -> Rarity:
    """Pick a rarity at random, weighted by drop weights. Pass a seeded rng for repeatable rolls."""
    weights = DROP_WEIGHTS if weights is None else weights
    validate_weights(weights)
    rng = _default_rng if rng is None else rng

    tiers = list(Rarity)
    return rng.choices(tiers, weights=[weights[tier] for tier in tiers])[0]


def quality_tags_for(rarity: Rarity) -> QualityTags:
    """Prompt additions for a rarity, for the image-generation job to use."""
    return QUALITY_TAGS[rarity]
