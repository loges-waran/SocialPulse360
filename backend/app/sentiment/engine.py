"""
Hybrid NLP Sentiment Analysis Engine for English, Tanglish, and Tamil.
Provides explainable rule-based valence scoring, negation & booster handling,
confidence calculation, and language tagging.
"""

import math
from typing import Dict, Any, List
from app.utils.text_utils import clean_text, detect_language
from app.sentiment.english_lexicon import ENGLISH_VALENCE, ENGLISH_BOOSTERS, ENGLISH_NEGATIONS
from app.sentiment.tanglish_lexicon import TANGLISH_VALENCE, TANGLISH_BOOSTERS, TANGLISH_NEGATIONS

class SentimentEngine:
    def __init__(self):
        # Combined Valence Dictionary
        self.valence_dict = {**ENGLISH_VALENCE, **TANGLISH_VALENCE}
        self.boosters = {**ENGLISH_BOOSTERS, **TANGLISH_BOOSTERS}
        self.negations = ENGLISH_NEGATIONS | TANGLISH_NEGATIONS
        
    def analyze(self, text: str) -> Dict[str, Any]:
        """
        Analyze sentiment of given text.
        Returns dictionary containing:
        - sentiment: 'positive' | 'negative' | 'neutral'
        - score: compound score between -1.0 and 1.0
        - confidence: confidence rating between 0.50 and 0.99
        - language: 'english' | 'tanglish' | 'tamil'
        - matched_tokens: list of words that contributed to the score
        """
        if not text or not isinstance(text, str) or not text.strip():
            return {
                "sentiment": "neutral",
                "score": 0.0,
                "confidence": 0.50,
                "language": "unknown",
                "matched_tokens": []
            }

        lang = detect_language(text)
        cleaned = clean_text(text, remove_stopwords=False, keep_hashtags=True).lower()
        words = cleaned.split()

        if not words:
            return {
                "sentiment": "neutral",
                "score": 0.0,
                "confidence": 0.50,
                "language": lang,
                "matched_tokens": []
            }

        total_valence = 0.0
        matched_tokens = []
        i = 0
        n = len(words)

        while i < n:
            word = words[i]
            val = 0.0
            matched_phrase = word
            step = 1

            # Check 2-word phrase first (e.g., "vera level")
            if i + 1 < n:
                bigram = f"{words[i]} {words[i+1]}"
                if bigram in self.valence_dict:
                    val = self.valence_dict[bigram]
                    matched_phrase = bigram
                    step = 2

            # Check single word if no bigram match
            if val == 0.0 and word in self.valence_dict:
                val = self.valence_dict[word]

            if val != 0.0:
                # Check for preceding intensifier/booster
                booster_val = 0.0
                if i > 0 and words[i-1] in self.boosters:
                    booster_val = self.boosters[words[i-1]]
                elif i + 1 < n and words[i+1] in self.boosters:
                    booster_val = self.boosters[words[i+1]]

                # Apply booster
                if booster_val > 0:
                    if val > 0:
                        val += booster_val * 2.0
                    else:
                        val -= booster_val * 2.0

                # Check for preceding or trailing negation (e.g. "not good" or "nalla illa")
                is_negated = False
                # Lookback up to 2 words
                for lookback in [1, 2]:
                    if i - lookback >= 0 and words[i - lookback] in self.negations:
                        is_negated = True
                        break
                # Lookahead for Tanglish postfix negation ("padam nalla illa")
                if not is_negated and i + step < n and words[i + step] in self.negations:
                    is_negated = True

                if is_negated:
                    val = -val * 0.75  # Invert and slightly soften

                total_valence += val
                matched_tokens.append({
                    "token": matched_phrase,
                    "valence": round(val, 2)
                })

            i += step

        # Normalize score into standard VADER-style compound score [-1.0, 1.0]
        # Formula: score / sqrt(score^2 + alpha) where alpha = 15
        alpha = 15.0
        compound = total_valence / math.sqrt((total_valence * total_valence) + alpha)
        compound = round(compound, 4)

        # Classification thresholds
        if compound >= 0.05:
            sentiment = "positive"
        elif compound <= -0.05:
            sentiment = "negative"
        else:
            sentiment = "neutral"

        # Calculate Confidence Score [0.50 - 0.99]
        if sentiment == "neutral":
            confidence = round(0.55 + max(0.0, 0.25 - abs(compound)), 2)
        else:
            confidence = round(min(0.98, 0.65 + (abs(compound) * 0.35)), 2)

        return {
            "sentiment": sentiment,
            "score": compound,
            "confidence": confidence,
            "language": lang,
            "matched_tokens": matched_tokens
        }

# Global singleton instance
sentiment_engine = SentimentEngine()
