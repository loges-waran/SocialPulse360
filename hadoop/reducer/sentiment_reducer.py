#!/usr/bin/env python3
"""
Hadoop Streaming Reducer: Sentiment Aggregation
Input: Sorted sentiment\t1
Output: sentiment\ttotal_count
"""
import sys

def main():
    current_sentiment = None
    current_count = 0

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        parts = line.split('\t')
        if len(parts) != 2:
            continue

        sentiment, count_str = parts
        try:
            count = int(count_str)
        except ValueError:
            continue

        if current_sentiment == sentiment:
            current_count += count
        else:
            if current_sentiment:
                print(f"{current_sentiment}\t{current_count}")
            current_sentiment = sentiment
            current_count = count

    if current_sentiment:
        print(f"{current_sentiment}\t{current_count}")

if __name__ == "__main__":
    main()
