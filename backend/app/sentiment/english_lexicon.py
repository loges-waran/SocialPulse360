"""
Curated English sentiment lexicon with valence ratings (-4 to +4)
and list of booster/intensifier terms and negators.
"""

ENGLISH_VALENCE = {
    # Strong Positive (+3, +4)
    "excellent": 3.5, "outstanding": 3.8, "superb": 3.5, "phenomenal": 3.8, 
    "masterpiece": 3.7, "brilliant": 3.4, "amazing": 3.2, "wonderful": 3.2,
    "fantastic": 3.2, "awesome": 3.0, "breakthrough": 3.2, "revolution": 3.0,
    "innovative": 2.8, "triumph": 3.0, "delight": 2.8, "flawless": 3.4,
    "perfect": 3.2, "love": 3.0, "thrilling": 3.0, "milestone": 2.5,
    "sustainable": 2.5, "achievement": 2.6, "celebrate": 2.5, "proud": 2.6,

    # Moderate Positive (+1, +2)
    "good": 1.9, "great": 2.4, "nice": 1.8, "happy": 2.1, "helpful": 1.8,
    "clean": 1.6, "fast": 1.7, "smooth": 1.8, "useful": 1.9, "promising": 1.7,
    "better": 1.5, "best": 2.8, "effective": 2.0, "efficient": 2.2, "boost": 1.9,
    "expand": 1.4, "improving": 1.8, "improved": 1.9, "progress": 2.0, "support": 1.5,
    "recommend": 2.2, "recommended": 2.3, "reliable": 2.2, "valuable": 2.0,

    # Moderate Negative (-1, -2)
    "bad": -2.0, "poor": -2.0, "slow": -1.5, "delay": -1.8, "delayed": -1.9,
    "issue": -1.4, "issues": -1.5, "problem": -1.7, "problems": -1.8,
    "flaw": -1.6, "struggle": -1.8, "concern": -1.3, "difficult": -1.4,
    "annoying": -2.0, "frustrated": -2.3, "frustrating": -2.2, "sad": -2.0,
    "loss": -2.0, "drop": -1.5, "broken": -2.2, "drain": -1.7, "fail": -2.4,
    "failed": -2.4, "failure": -2.5, "late": -1.5, "damage": -2.2, "damaged": -2.3,

    # Strong Negative (-3, -4)
    "terrible": -3.4, "horrible": -3.5, "worst": -3.8, "disaster": -3.5,
    "disastrous": -3.6, "scam": -3.8, "fraud": -3.8, "disappointed": -2.8,
    "disappointing": -2.9, "awful": -3.3, "crap": -3.0, "useless": -3.1,
    "waste": -2.8, "crisis": -3.0, "catastrophe": -3.6, "sickening": -3.5,
    "crash": -2.8, "crashed": -2.8, "outage": -2.5, "ruined": -3.2,
    "hate": -3.2, "hateful": -3.4, "layoffs": -2.6, "gridlock": -2.4
}

ENGLISH_BOOSTERS = {
    "very": 0.35, "extremely": 0.5, "incredibly": 0.45, "really": 0.3,
    "completely": 0.35, "totally": 0.35, "super": 0.4, "highly": 0.35,
    "truly": 0.3, "deeply": 0.3, "absolutely": 0.4, "so": 0.25
}

ENGLISH_NEGATIONS = {
    "not", "no", "never", "none", "neither", "nor", "hardly", "barely",
    "cannot", "can't", "don't", "didn't", "won't", "isn't", "aren't",
    "wasn't", "weren't", "without"
}
