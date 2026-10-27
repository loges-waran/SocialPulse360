#!/usr/bin/env python3
"""
Hadoop Streaming Reducer: Daily Sentiment Trends
Input: Sorted YYYY-MM-DD:sentiment\t1
Output: YYYY-MM-DD:sentiment\ttotal_count
"""
import sys

def main():
    current_key = None
    current_count = 0

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        parts = line.split('\t')
        if len(parts) != 2:
            continue

        key, count_str = parts
        try:
            count = int(count_str)
        except ValueError:
            continue

        if current_key == key:
            current_count += count
        else:
            if current_key:
                print(f"{current_key}\t{current_count}")
            current_key = key
            current_count = count

    if current_key:
        print(f"{current_key}\t{current_count}")

if __name__ == "__main__":
    main()
