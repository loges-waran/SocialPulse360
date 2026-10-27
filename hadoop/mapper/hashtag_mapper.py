#!/usr/bin/env python3
"""
Hadoop Streaming Mapper: Hashtag Frequency Counter
Input: Standard input lines
Output: #hashtag\t1
"""
import sys
import re

HASHTAG_REGEX = re.compile(r'#(\w+)')

def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        
        matches = HASHTAG_REGEX.findall(line)
        for tag in matches:
            normalized_tag = tag.lower()
            print(f"#{normalized_tag}\t1")

if __name__ == "__main__":
    main()
