"""
Curated Tanglish (Tamil-English transliterated) and Tamil Unicode sentiment lexicon
with valence scores (-4 to +4), boosters, and negations.
"""

TANGLISH_VALENCE = {
    # Tanglish Positive Terms (+1.5 to +4.0)
    "semma": 3.4,
    "mass": 3.2,
    "vera level": 3.8,
    "veralevel": 3.8,
    "tharumaru": 3.5,
    "tharam": 3.0,
    "super": 2.8,
    "nalla": 2.2,
    "nallathu": 2.3,
    "azhaga": 2.5,
    "azhagu": 2.5,
    "magizhchi": 3.0,
    "perumai": 3.0,
    "vetri": 3.0,
    "vaalthukkal": 3.2,
    "asathal": 3.0,
    "kalakkal": 3.0,
    "kondattam": 2.8,
    "arputham": 3.5,
    "sirappu": 2.8,
    "gubeer": 2.2, # comedy laughter
    "thee": 2.5, # fire/lit
    "jhakaas": 2.5,
    "alapparai": 2.4,
    "podu": 1.8,
    "whistle": 2.0,

    # Tanglish Negative Terms (-1.5 to -4.0)
    "mokka": -3.2,
    "waste": -3.0,
    "karumam": -3.6,
    "mosam": -3.2,
    "kevalam": -3.5,
    "kevalamana": -3.6,
    "kodumai": -3.4,
    "kashtam": -2.6,
    "tholvi": -3.0,
    "sothappal": -2.8,
    "sothapals": -2.8,
    "kaduppu": -3.0,
    "yerichal": -3.0,
    "avasthai": -3.0,
    "thalaivali": -2.6,
    "cringe": -2.8,
    "uruttu": -2.6,
    "thappu": -2.4,
    "alatchiyam": -3.0,
    "alukku": -2.4,
    "mosamana": -3.4,
    "valikithu": -2.5,
    "bayam": -2.2,

    # Tamil Unicode Positive
    "அருமை": 3.2,
    "அருமையான": 3.4,
    "சிறப்பு": 2.8,
    "சிறப்பான": 3.0,
    "வெற்றி": 3.0,
    "மகிழ்ச்சி": 3.2,
    "பாராட்டுக்கள்": 3.2,
    "வாழ்த்துக்கள்": 3.2,
    "நன்று": 2.5,
    "முன்னேற்றம்": 2.8,
    "தூய்மை": 2.4,
    "பயனுள்ளது": 2.6,

    # Tamil Unicode Negative
    "மோசமான": -3.5,
    "மோசம்": -3.2,
    "வீண்": -3.0,
    "தோல்வி": -3.2,
    "அவதி": -3.0,
    "சீர்கேடு": -3.4,
    "தாமதம்": -2.5,
    "தவறு": -2.5,
    "ஏமாற்றம்": -3.2,
    "கேவலம்": -3.6
}

TANGLISH_BOOSTERS = {
    "romba": 0.4,
    "semmaya": 0.45,
    "bayangara": 0.4,
    "periya": 0.3,
    "athigama": 0.3,
    "migavum": 0.4,  # Tamil Unicode transliterated
    "மிகவும்": 0.4    # Tamil Unicode
}

TANGLISH_NEGATIONS = {
    "illa", "illatha", "mudiyala", "kedaikala", "maatudhu", "pannaama",
    "varaathu", "illai", "இல்லை"
}
