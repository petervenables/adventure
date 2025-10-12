"""adventure/constants."""

SELF_WORDS = ["me", "myself", "I", "self"]
VISIBILITY_MOD_WORDS = ["at", "around", "into", "over", "about"]
MOBILITY_MOD_WORDS = ["to", "the", "towards", "near", "from", "with", "by", "on", "off"]
LOCATION_MOD_WORDS = [
    "to",
    "into",
    "out",
    "over",
    "under",
    "above",
    "below",
    "around",
    "through",
]
# separators split multiword tokens (articles + common prepositions)
SEPARATORS = {
    "the", "a", "an",   # articles
    "at", "to", "in", "on", "into", "onto", "from", "with", "by", "inside",
    "outside", "through", "over", "under", "against", "upon", "of",
    "toward", "towards", "about", "as", "for"
}

PREPOSITIONS = {
    "at", "to", "in", "on", "into", "onto", "from", "with", "by", "inside",
    "outside", "through", "over", "under", "against", "upon", "of",
    "toward", "towards", "about", "as", "for"
}