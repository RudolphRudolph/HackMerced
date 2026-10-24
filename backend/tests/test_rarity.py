import random
from collections import Counter

import pytest

from app.config import DROP_WEIGHTS, QUALITY_TAGS
from app.models import QualityTags, Rarity
from app.rarity import RarityConfigError, roll_rarity, validate_weights

VALID_WEIGHTS = {tier: 1.0 for tier in Rarity}


def test_seeded_rng_gives_same_rolls():
    rng_a, rng_b = random.Random(1234), random.Random(1234)
    assert [roll_rarity(rng_a) for _ in range(100)] == [roll_rarity(rng_b) for _ in range(100)]


def test_frequencies_match_configured_weights():
    rng = random.Random(0)
    n = 100_000
    counts = Counter(roll_rarity(rng) for _ in range(n))
    total = sum(DROP_WEIGHTS.values())

    for tier in Rarity:
        assert counts[tier] / n == pytest.approx(DROP_WEIGHTS[tier] / total, abs=0.01)


def test_zero_weight_tier_never_rolls():
    weights = {**VALID_WEIGHTS, Rarity.RED: 0}
    rng = random.Random(0)
    assert Rarity.RED not in {roll_rarity(rng, weights) for _ in range(10_000)}


def test_every_rarity_has_quality_tags():
    assert set(QUALITY_TAGS) == set(Rarity)
    assert all(isinstance(tags, QualityTags) for tags in QUALITY_TAGS.values())


def test_shipped_weights_are_valid():
    validate_weights(DROP_WEIGHTS)


@pytest.mark.parametrize(
    ("weights", "message"),
    [
        ({}, "empty"),
        ({Rarity.GREEN: 1}, "BLUE"),
        ({**VALID_WEIGHTS, "purple": 1}, "purple"),
        ({**VALID_WEIGHTS, Rarity.RED: -1}, "RED"),
        ({**VALID_WEIGHTS, Rarity.RED: float("nan")}, "RED"),
        ({**VALID_WEIGHTS, Rarity.RED: "5"}, "RED"),
        ({tier: 0 for tier in Rarity}, "greater than 0"),
    ],
    ids=["empty", "missing-tier", "unknown-key", "negative", "nan", "not-a-number", "all-zero"],
)
def test_invalid_weights_raise_clear_error(weights, message):
    with pytest.raises(RarityConfigError, match=message):
        roll_rarity(random.Random(0), weights)
