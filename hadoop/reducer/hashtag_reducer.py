#!/usr/bin/env python3
"""
Hadoop Streaming Reducer: Hashtag Frequency Counter
Input: Sorted #hashtag\t1 pairs
Output: #hashtag\ttotal_count
"""
import sys

def main():
    current_tag = None
    current_count = 0

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        parts = line.split('\t')
        if len(parts) != 2:
            continue

        tag, count_str = parts
        try:
            count = int(count_str)
        except ValueError:
            continue

        if current_tag == tag:
            current_count += count
        else:
            if current_tag:
                print(f"{current_tag}\t{current_count}")
            current_tag = tag
            current_count = count

    if current_tag:
        print(f"{current_tag}\t{current_count}")

if __name__ == "__main__":
    main()
