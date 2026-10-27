#!/usr/bin/env python3
"""
Hadoop Streaming Mapper: Word Count
Input: Standard input lines (Text or CSV rows)
Output: word\t1
"""
import sys
import re

if hasattr(sys.stdin, "reconfigure"):
    sys.stdin.reconfigure(encoding="utf-8", errors="replace")
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

STOP_WORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", 
    "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", 
    "by", "can", "did", "do", "does", "doing", "down", "during", "each", "few", "for", "from", 
    "had", "has", "have", "he", "her", "here", "him", "his", "how", "i", "if", "in", "into", 
    "is", "it", "its", "just", "me", "more", "most", "my", "no", "nor", "not", "now", "of", 
    "off", "on", "once", "only", "or", "other", "our", "out", "over", "own", "same", "she", 
    "should", "so", "some", "such", "than", "that", "the", "their", "them", "then", "there", 
    "these", "they", "this", "those", "through", "to", "too", "under", "until", "up", "very", 
    "was", "we", "were", "what", "when", "where", "which", "while", "who", "whom", "why", "with", 
    "would", "you", "your", "da", "di", "ah", "la", "bro", "intha", "antha", "enna", "irukku", 
    "aachu", "pochu", "nu", "oru", "romba", "https", "http", "rt"
}

DATE_TIME_REGEX = re.compile(r'^\d{4}-\d{2}-\d{2}$|^\d{2}:\d{2}:\d{2}$')

def clean_token(token):
    return re.sub(r'[^\w\u0B80-\u0BFF]', '', token.strip().lower())

def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        # Split tokens by whitespace or comma
        tokens = re.split(r'[\s,"]+', line)
        for token in tokens:
            token = token.strip()
            if not token or token.startswith('@') or DATE_TIME_REGEX.match(token):
                continue
            cleaned = clean_token(token)
            if cleaned and len(cleaned) > 2 and not cleaned.isdigit() and cleaned not in STOP_WORDS:
                print(f"{cleaned}\t1")

if __name__ == "__main__":
    main()
