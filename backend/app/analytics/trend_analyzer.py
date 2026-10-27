"""
Trend Analyzer Service.
Computes and aggregates analytics summaries from MapReduce job outputs
and cleaned dataset records.
"""

from typing import Dict, Any, List
import pandas as pd

class TrendAnalyzer:
    def aggregate_word_trends(self, wordcount_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Formats word frequencies into Top 10, 20, 50."""
        # Sort descending by value
        sorted_words = sorted(wordcount_results, key=lambda x: x["value"], reverse=True)
        return {
            "top_10": sorted_words[:10],
            "top_20": sorted_words[:20],
            "top_50": sorted_words[:50],
            "total_unique_words": len(sorted_words)
        }

    def aggregate_hashtags(self, hashtag_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Formats top hashtags sorted descending."""
        sorted_tags = sorted(hashtag_results, key=lambda x: x["value"], reverse=True)
        return sorted_tags[:30]

    def aggregate_sentiment_words(self, sentiment_words_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Parses results formatted as sentiment:word -> count
        Groups into positive keywords and negative keywords.
        """
        pos_words = {}
        neg_words = {}
        neu_words = {}

        for item in sentiment_words_results:
            key = item["key"]
            count = item["value"]
            if ":" in key:
                sent, word = key.split(":", 1)
                sent = sent.lower()
                if sent == "positive":
                    pos_words[word] = pos_words.get(word, 0) + count
                elif sent == "negative":
                    neg_words[word] = neg_words.get(word, 0) + count
                else:
                    neu_words[word] = neu_words.get(word, 0) + count

        sorted_pos = [{"word": k, "count": v} for k, v in sorted(pos_words.items(), key=lambda x: x[1], reverse=True)]
        sorted_neg = [{"word": k, "count": v} for k, v in sorted(neg_words.items(), key=lambda x: x[1], reverse=True)]
        sorted_neu = [{"word": k, "count": v} for k, v in sorted(neu_words.items(), key=lambda x: x[1], reverse=True)]

        return {
            "positive_keywords": sorted_pos[:20],
            "negative_keywords": sorted_neg[:20],
            "neutral_keywords": sorted_neu[:20]
        }

    def aggregate_daily_trends(self, daily_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Parses YYYY-MM-DD:sentiment -> count into structured timeline records:
        [{"date": "2026-10-20", "positive": 5, "negative": 2, "neutral": 1, "total": 8}, ...]
        """
        daily_dict = {}

        for item in daily_results:
            key = item["key"]
            count = item["value"]
            if ":" in key:
                date_str, sentiment = key.split(":", 1)
                sentiment = sentiment.lower()
                if date_str not in daily_dict:
                    daily_dict[date_str] = {"date": date_str, "positive": 0, "negative": 0, "neutral": 0, "total": 0}
                if sentiment in daily_dict[date_str]:
                    daily_dict[date_str][sentiment] += count
                    daily_dict[date_str]["total"] += count

        sorted_timeline = sorted(daily_dict.values(), key=lambda x: x["date"])
        return sorted_timeline

    def calculate_sentiment_distribution(self, sentiment_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculates exact count and percentage for positive, negative, neutral."""
        counts = {"positive": 0, "negative": 0, "neutral": 0}
        total = 0

        for item in sentiment_results:
            sent = item["key"].lower()
            val = item["value"]
            if sent in counts:
                counts[sent] = val
                total += val

        percentages = {}
        for k, v in counts.items():
            percentages[k] = round((v / total * 100), 2) if total > 0 else 0.0

        return {
            "counts": counts,
            "percentages": percentages,
            "total_records": total
        }

trend_analyzer = TrendAnalyzer()
