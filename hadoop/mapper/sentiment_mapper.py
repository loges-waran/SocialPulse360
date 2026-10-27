#!/usr/bin/env python3
"""
Hadoop Streaming Mapper: Sentiment Aggregation
Input: Preprocessed records or raw text lines
Output: sentiment_label\t1
"""
import sys
import re

# Key valence indicators for streaming Hadoop mapper
POSITIVE_WORDS = {
    "semma", "mass", "super", "vera", "level", "veralevel", "nalla", "azhaga", 
    "azhagu", "magizhchi", "perumai", "vetri", "vaalthukkal", "good", "great", 
    "awesome", "excellent", "clean", "fast", "useful", "breakthrough", "innovation",
    "sustainable", "improved", "recommend", "அருமை", "சிறப்பு", "வெற்றி", "மகிழ்ச்சி"
}

NEGATIVE_WORDS = {
    "mokka", "waste", "karumam", "mosam", "kevalam", "kodumai", "kashtam", "tholvi", 
    "kaduppu", "bad", "poor", "slow", "delay", "delayed", "issue", "worst", 
    "disaster", "scam", "fraud", "disappointed", "useless", "broken", "fail", 
    "failed", "failure", "outage", "crashed", "மோசமான", "வீண்", "தோல்வி", "அவதி"
}

def determine_sentiment(text):
    text_lower = text.lower()
    pos_score = sum(1 for w in POSITIVE_WORDS if w in text_lower)
    neg_score = sum(1 for w in NEGATIVE_WORDS if w in text_lower)
    if pos_score > neg_score:
        return "positive"
    elif neg_score > pos_score:
        return "negative"
    else:
        return "neutral"

def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        
        # Check if input is a structured TSV with labeled sentiment
        parts = line.split('\t')
        sentiment = None
        for p in parts:
            p_clean = p.strip().lower()
            if p_clean in ("positive", "negative", "neutral"):
                sentiment = p_clean
                break
        
        if not sentiment:
            sentiment = determine_sentiment(line)
            
        print(f"{sentiment}\t1")

if __name__ == "__main__":
    main()
