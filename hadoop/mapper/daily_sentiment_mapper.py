#!/usr/bin/env python3
"""
Hadoop Streaming Mapper: Daily Sentiment Trends
Input: Tab-separated records containing timestamp and sentiment or text
Output: YYYY-MM-DD:sentiment\t1
"""
import sys
import re

DATE_REGEX = re.compile(r'(\d{4}-\d{2}-\d{2})')

def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        parts = line.split('\t')
        date_str = None
        sentiment = "neutral"

        # Search for date in parts
        for p in parts:
            date_match = DATE_REGEX.search(p)
            if date_match:
                date_str = date_match.group(1)
                break

        # Search for sentiment in parts
        for p in parts:
            p_clean = p.strip().lower()
            if p_clean in ("positive", "negative", "neutral"):
                sentiment = p_clean
                break

        if date_str:
            print(f"{date_str}:{sentiment}\t1")

if __name__ == "__main__":
    main()
