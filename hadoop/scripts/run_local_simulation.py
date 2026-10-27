#!/usr/bin/env python3
"""
SocialPulse 360 - Standalone Local MapReduce Runner
Executes MapReduce jobs locally using standard pipes (Mapper | Sort | Reducer),
emulating Hadoop Streaming behavior for offline or educational environments.

Usage:
    python run_local_simulation.py --job wordcount --input ../../backend/data/sample/sample_social_tanglish_english.csv
    python run_local_simulation.py --job hashtag
    python run_local_simulation.py --job sentiment
    python run_local_simulation.py --job daily
    python run_local_simulation.py --job sentiment_words
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MAPPER_DIR = BASE_DIR / "mapper"
REDUCER_DIR = BASE_DIR / "reducer"
OUTPUT_DIR = BASE_DIR / "sample_output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

JOB_CONFIG = {
    "wordcount": ("wordcount_mapper.py", "wordcount_reducer.py", "wordcount_output.txt"),
    "hashtag": ("hashtag_mapper.py", "hashtag_reducer.py", "hashtag_output.txt"),
    "sentiment": ("sentiment_mapper.py", "sentiment_reducer.py", "sentiment_output.txt"),
    "daily": ("daily_sentiment_mapper.py", "daily_sentiment_reducer.py", "daily_sentiment_output.txt"),
    "sentiment_words": ("sentiment_words_mapper.py", "sentiment_words_reducer.py", "sentiment_words_output.txt")
}

def run_job(job_name, input_file):
    if job_name not in JOB_CONFIG:
        print(f"Unknown job '{job_name}'. Available: {list(JOB_CONFIG.keys())}")
        sys.exit(1)

    mapper_file, reducer_file, out_file = JOB_CONFIG[job_name]
    mapper_path = MAPPER_DIR / mapper_file
    reducer_path = REDUCER_DIR / reducer_file
    output_path = OUTPUT_DIR / out_file

    if not Path(input_file).exists():
        print(f"Input file not found: {input_file}")
        sys.exit(1)

    print(f"\n=======================================================")
    print(f"  SocialPulse 360: Local MapReduce Engine Simulation")
    print(f"  Job: {job_name.upper()}")
    print(f"  Mapper: {mapper_file}")
    print(f"  Reducer: {reducer_file}")
    print(f"  Input: {input_file}")
    print(f"  Output: {output_path}")
    print(f"=======================================================\n")

    with open(input_file, "r", encoding="utf-8", errors="ignore") as f:
        input_data = f.read()

    # Step 1: Map Phase
    print("[1/3] Executing Map Phase...")
    py_exec = sys.executable
    sub_env = {**os.environ, "PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1"}
    map_proc = subprocess.Popen(
        [py_exec, str(mapper_path)],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=sub_env
    )
    map_out, map_err = map_proc.communicate(input=input_data)
    if map_proc.returncode != 0:
        print(f"Mapper Error:\n{map_err}")
        sys.exit(1)

    map_lines = [l.strip() for l in map_out.splitlines() if l.strip()]
    print(f"      -> Map emitted {len(map_lines)} key-value pairs.")

    # Step 2: Sort and Shuffle Phase
    print("[2/3] Executing Sort & Shuffle Phase (Grouping keys)...")
    sorted_map_lines = sorted(map_lines)
    unique_keys = set([l.split('\t')[0] for l in sorted_map_lines if '\t' in l])
    print(f"      -> Partitioned into {len(unique_keys)} distinct keys.")

    # Step 3: Reduce Phase
    print("[3/3] Executing Reduce Phase...")
    red_proc = subprocess.Popen(
        [py_exec, str(reducer_path)],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=sub_env
    )
    red_input = "\n".join(sorted_map_lines) + "\n"
    red_out, red_err = red_proc.communicate(input=red_input)
    if red_proc.returncode != 0:
        print(f"Reducer Error:\n{red_err}")
        sys.exit(1)

    reduce_lines = [l.strip() for l in red_out.splitlines() if l.strip()]
    print(f"      -> Reducer completed with {len(reduce_lines)} aggregated outputs.\n")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(reduce_lines))

    print("Sample Output (Top 10):")
    print("-------------------------------------------------------")
    for line in reduce_lines[:10]:
        print(f"  {line}")
    print("-------------------------------------------------------")
    print(f"Results successfully saved to: {output_path}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SocialPulse 360 Local MapReduce Simulation")
    parser.add_argument("--job", choices=["wordcount", "hashtag", "sentiment", "daily", "sentiment_words"], default="wordcount")
    parser.add_argument("--input", default=str(BASE_DIR.parent / "backend" / "data" / "sample" / "sample_social_tanglish_english.csv"))
    args = parser.parse_args()

    run_job(args.job, args.input)
