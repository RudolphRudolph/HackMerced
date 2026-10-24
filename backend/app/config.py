"""Tunable rarity settings. Edit values here; the logic lives in rarity.py."""

from app.models import QualityTags, Rarity

# TODO: placeholder odds, not final.
# Relative weights: they don't need to sum to 100. Rarer tiers get lower weights; 0 disables a tier.
DROP_WEIGHTS: dict[Rarity, float] = {
    Rarity.GREEN: 50,
    Rarity.BLUE: 25,
    Rarity.YELLOW: 15,
    Rarity.GOLD: 8,
    Rarity.RED: 2,
}

# Quality tags added to the Animagine XL 4.0 prompt for each tier.
# Rarity only changes image quality, never the character itself.
QUALITY_TAGS: dict[Rarity, QualityTags] = {
    Rarity.GREEN: QualityTags(
        positive="worst quality, low quality, low score",
        negative="",
    ),
    # TODO: decide Blue tags.
    Rarity.BLUE: QualityTags(positive="", negative=""),
    # TODO: decide Yellow tags.
    Rarity.YELLOW: QualityTags(positive="", negative=""),
    Rarity.GOLD: QualityTags(
        positive="masterpiece, best quality, high score, great score, absurdres",
        negative="worst quality, low quality, low score, bad score, lowres, blurry",
    ),
    # TODO: decide Red tags. Red is the rarest tier, but Gold currently has the top-quality tags.
    Rarity.RED: QualityTags(positive="", negative=""),
}
