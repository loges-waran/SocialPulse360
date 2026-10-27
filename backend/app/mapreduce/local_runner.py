"""
Local MapReduce Execution Framework.
Simulates Hadoop MapReduce architecture with strict separation of:
1. Input Splitting
2. Map Phase (streaming to mapper script)
3. Shuffle & Sort Phase (sorting keys, partitioning)
4. Reduce Phase (streaming sorted keys to reducer script)
5. Metric Collection (Map Input, Map Output, Reduce Input, Reduce Output, Duration)
"""

import sys
import subprocess
import time
from pathlib import Path
from typing import Dict, Any, List
from app.config import MAPPER_DIR, REDUCER_DIR, PROCESSED_DATA_DIR

class LocalMapReduceRunner:
    def __init__(self):
        self.mapper_dir = MAPPER_DIR
        self.reducer_dir = REDUCER_DIR
        self.output_dir = PROCESSED_DATA_DIR / "mapreduce_output"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def run_job(self, job_name: str, mapper_script: str, reducer_script: str, input_data: str) -> Dict[str, Any]:
        """
        Executes a MapReduce job locally via subprocess pipes, exactly matching
        Hadoop Streaming architecture.
        """
        start_time = time.perf_counter()
        mapper_path = self.mapper_dir / mapper_script
        reducer_path = self.reducer_dir / reducer_script

        if not mapper_path.exists():
            raise FileNotFoundError(f"Mapper script not found: {mapper_path}")
        if not reducer_path.exists():
            raise FileNotFoundError(f"Reducer script not found: {reducer_path}")

        lines = [line.strip() for line in input_data.splitlines() if line.strip()]
        map_input_records = len(lines)

        # -----------------------------
        # Phase 1: MAP PHASE
        # Pipe input_data lines into Mapper's STDIN
        # -----------------------------
        python_exec = sys.executable
        import os
        sub_env = {**os.environ, "PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1"}
        map_proc = subprocess.Popen(
            [python_exec, str(mapper_path)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=sub_env
        )
        map_stdout, map_stderr = map_proc.communicate(input=input_data)

        if map_proc.returncode != 0:
            raise RuntimeError(f"Mapper failed with error: {map_stderr}")

        map_output_lines = [line.strip() for line in map_stdout.splitlines() if line.strip()]
        map_output_records = len(map_output_lines)

        # -----------------------------
        # Phase 2: SORT & SHUFFLE PHASE
        # Hadoop framework sorts map output lines alphabetically by key
        # -----------------------------
        # Each line is "key\tvalue"
        sorted_map_output = sorted(map_output_lines)
        unique_keys = set()
        for line in sorted_map_output:
            parts = line.split('\t')
            if parts:
                unique_keys.add(parts[0])
        shuffle_keys_count = len(unique_keys)

        sorted_input_for_reducer = "\n".join(sorted_map_output) + "\n"

        # -----------------------------
        # Phase 3: REDUCE PHASE
        # Pipe sorted mapper output into Reducer's STDIN
        # -----------------------------
        red_proc = subprocess.Popen(
            [python_exec, str(reducer_path)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=sub_env
        )
        red_stdout, red_stderr = red_proc.communicate(input=sorted_input_for_reducer)

        if red_proc.returncode != 0:
            raise RuntimeError(f"Reducer failed with error: {red_stderr}")

        reduce_output_lines = [line.strip() for line in red_stdout.splitlines() if line.strip()]
        reduce_output_records = len(reduce_output_lines)

        duration_ms = round((time.perf_counter() - start_time) * 1000, 2)

        # Save output to disk
        out_filename = f"{job_name.lower()}_output.txt"
        out_path = self.output_dir / out_filename
        with open(out_path, "w", encoding="utf-8") as f:
            f.write("\n".join(reduce_output_lines))

        # Parse key-values
        parsed_results = []
        for line in reduce_output_lines:
            parts = line.split('\t')
            if len(parts) == 2:
                key, val = parts
                try:
                    val_num = int(val)
                except ValueError:
                    val_num = val
                parsed_results.append({"key": key, "value": val_num})

        return {
            "job_name": job_name,
            "execution_mode": "Local MapReduce (Hadoop Architecture Simulation)",
            "status": "COMPLETED",
            "duration_ms": duration_ms,
            "metrics": {
                "map_input_records": map_input_records,
                "map_output_records": map_output_records,
                "shuffle_keys_count": shuffle_keys_count,
                "reduce_input_records": map_output_records,
                "reduce_output_records": reduce_output_records
            },
            "output_file": str(out_path.name),
            "sample_output": reduce_output_lines[:25],
            "parsed_results": parsed_results
        }

# Global runner
local_mr_runner = LocalMapReduceRunner()
