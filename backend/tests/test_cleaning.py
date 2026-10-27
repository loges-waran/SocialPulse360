"""
Unit tests for text preprocessing, cleaning, and language detection.
"""

from app.utils.text_utils import clean_text, extract_hashtags, detect_language, tokenize_words

def test_clean_text_removes_urls_and_handles():
    raw = "Check out https://example.com/test and @chennaite_07 for updates! #Tech"
    cleaned = clean_text(raw, remove_stopwords=False, keep_hashtags=False)
    assert "https" not in cleaned
    assert "@chennaite_07" not in cleaned
    assert "Tech" in cleaned

def test_extract_hashtags():
    text = "Great progress on #DigitalIndia and #SDG9 innovation!"
    tags = extract_hashtags(text)
    assert "digitalindia" in tags
    assert "sdg9" in tags

def test_language_detection():
    tanglish_text = "Intha padam semma mass ah irukku vera level!"
    english_text = "Modern cloud computing improves distributed big data workflows."
    tamil_text = "மிகவும் அருமையான முயற்சி வாழ்த்துக்கள்"

    assert detect_language(tanglish_text) == "tanglish"
    assert detect_language(english_text) == "english"
    assert detect_language(tamil_text) == "tamil"

def test_tokenize_words():
    text = "Big data analytics with Hadoop and MapReduce distributed processing."
    tokens = tokenize_words(text, remove_stopwords=True)
    assert "analytics" in tokens
    assert "hadoop" in tokens
    assert "mapreduce" in tokens
    assert "and" not in tokens
