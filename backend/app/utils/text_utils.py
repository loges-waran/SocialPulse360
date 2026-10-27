import re
import string

# Common English Stop Words
ENGLISH_STOP_WORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", 
    "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", 
    "by", "can", "did", "do", "does", "doing", "down", "during", "each", "few", "for", "from", 
    "further", "had", "has", "have", "having", "he", "her", "here", "hers", "herself", "him", 
    "himself", "his", "how", "i", "if", "in", "into", "is", "it", "its", "itself", "just", 
    "me", "more", "most", "my", "myself", "no", "nor", "not", "now", "of", "off", "on", "once", 
    "only", "or", "other", "our", "ours", "ourselves", "out", "over", "own", "same", "she", 
    "should", "so", "some", "such", "than", "that", "the", "their", "theirs", "them", 
    "themselves", "then", "there", "these", "they", "this", "those", "through", "to", "too", 
    "under", "until", "up", "very", "was", "we", "were", "what", "when", "where", "which", 
    "while", "who", "whom", "why", "with", "would", "you", "your", "yours", "yourself", 
    "yourselves"
}

# Common Tanglish Stop Words & Particles
TANGLISH_STOP_WORDS = {
    "da", "di", "ah", "la", "pa", "bro", "machan", "intha", "antha", "enna", "ethu", 
    "avan", "aval", "avanga", "naan", "neenga", "namma", "kooda", "mela", "keezha", 
    "irukku", "iruku", "irukan", "irukaanga", "panna", "pannu", "pannunga", "mudiyala", 
    "varala", "pochu", "aachu", "aachu", "nu", "endru", "oru", "theriyum", "theriyala", 
    "romba", "konjam", "mattum"
}

# Tamil Unicode range: U+0B80 to U+0BFF
TAMIL_UNICODE_REGEX = re.compile(r'[\u0B80-\u0BFF]')

# Tanglish marker tokens
TANGLISH_MARKERS = {
    "semma", "vera", "level", "mokka", "mass", "tharumaru", "padam", "kodumai", 
    "mosam", "azhaga", "azhagu", "magizhchi", "perumai", "innaiku", "naalaiku", 
    "nalla", "kedaikave", "mudiyala", "panranga", "thala", "thalapathy", "vada", 
    "podu", "paathu", "therila", "karumam", "kevalam", "uruttu"
}

URL_REGEX = re.compile(r'https?://\S+|www\.\S+')
MENTION_REGEX = re.compile(r'@\w+')
HASHTAG_REGEX = re.compile(r'#(\w+)')
WHITESPACE_REGEX = re.compile(r'\s+')

def extract_hashtags(text: str) -> list[str]:
    """Extract hashtags from raw text preserving case."""
    if not text or not isinstance(text, str):
        return []
    return [match.group(1).lower() for match in HASHTAG_REGEX.finditer(text)]

def detect_language(text: str) -> str:
    """
    Detect whether the text is English, Tamil script, Tanglish (Tamil-English),
    or Mixed.
    """
    if not text or not isinstance(text, str):
        return "unknown"
    
    # Check for Tamil Unicode characters
    tamil_chars = TAMIL_UNICODE_REGEX.findall(text)
    if len(tamil_chars) > 3:
        return "tamil"
    
    # Check for Tanglish token markers
    words = [w.lower().strip(string.punctuation) for w in text.split()]
    tanglish_matches = [w for w in words if w in TANGLISH_MARKERS or w in TANGLISH_STOP_WORDS]
    
    if len(tanglish_matches) >= 2 or (len(tanglish_matches) >= 1 and len(words) <= 6):
        return "tanglish"
    
    return "english"

def clean_text(text: str, remove_stopwords: bool = False, keep_hashtags: bool = True) -> str:
    """
    Cleans raw social media text:
    - Removes URLs
    - Normalizes mentions
    - Strips or normalizes hashtags
    - Cleans punctuation and excessive whitespace
    - Preserves casing or converts to lowercase for tokenization
    """
    if not text or not isinstance(text, str):
        return ""

    # Remove URLs
    cleaned = URL_REGEX.sub('', text)

    # Remove User Mentions
    cleaned = MENTION_REGEX.sub('', cleaned)

    if not keep_hashtags:
        cleaned = HASHTAG_REGEX.sub(r'\1', cleaned)
    else:
        # Keep word after hashtag
        cleaned = HASHTAG_REGEX.sub(r' \1 ', cleaned)

    # Retain Tamil Unicode, English alphanumeric characters, and basic spaces
    # Replace punctuation with spaces
    cleaned = re.sub(r'[^\w\s\u0B80-\u0BFF]', ' ', cleaned)

    # Normalize multiple whitespace
    cleaned = WHITESPACE_REGEX.sub(' ', cleaned).strip()

    if remove_stopwords:
        tokens = cleaned.split()
        tokens = [
            t for t in tokens 
            if t.lower() not in ENGLISH_STOP_WORDS and t.lower() not in TANGLISH_STOP_WORDS and len(t) > 1
        ]
        cleaned = ' '.join(tokens)

    return cleaned

def tokenize_words(text: str, remove_stopwords: bool = True) -> list[str]:
    """Tokenize text into cleaned words for MapReduce word counting."""
    cleaned = clean_text(text, remove_stopwords=remove_stopwords)
    words = [w.lower() for w in cleaned.split() if len(w) > 2 and not w.isdigit()]
    return words
