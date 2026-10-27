#!/usr/bin/env python3
"""
Hadoop Streaming Reducer: Word Count
Input: Sorted key\tvalue pairs from mapper
Output: word\ttotal_count
"""
import sys

if hasattr(sys.stdin, "reconfigure"):
    sys.stdin.reconfigure(encoding="utf-8", errors="replace")
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

def main():
    current_word = None
    current_count = 0

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        parts = line.split('\t')
        if len(parts) != 2:
            continue

        word, count_str = parts
        try:
            count = int(count_str)
        except ValueError:
            continue

        if current_word == word:
            current_count += count
        else:
            if current_word:
                print(f"{current_word}\t{current_count}")
            current_word = word
            current_count = count

    # Output last key
    if current_word:
        print(f"{current_word}\t{current_count}")

if __name__ == "__main__":
    main()
