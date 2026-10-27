"""
MapReduce Monitoring and Inspector API Routes.
Provides full observability into the 5 MapReduce job executions,
metrics, and source mapper/reducer code inspection.
"""

from pathlib import Path
from fastapi import APIRouter, HTTPException
from app.services.pipeline_runner import pipeline_runner
from app.config import MAPPER_DIR, REDUCER_DIR

router = APIRouter(prefix="/api/mapreduce", tags=["MapReduce"])

JOB_SCRIPT_MAP = {
    "wordcount": ("wordcount_mapper.py", "wordcount_reducer.py"),
    "hashtags": ("hashtag_mapper.py", "hashtag_reducer.py"),
    "sentiment": ("sentiment_mapper.py", "sentiment_reducer.py"),
    "daily": ("daily_sentiment_mapper.py", "daily_sentiment_reducer.py"),
    "sentiment_words": ("sentiment_words_mapper.py", "sentiment_words_reducer.py")
}

@router.get("/jobs")
def get_mapreduce_jobs():
    """
    Returns telemetry for all 5 executed MapReduce jobs:
    Map Input, Map Output, Shuffle Keys Count, Reduce Input, Reduce Output, Duration, and Output previews.
    """
    state = pipeline_runner.get_active_state()
    if not state:
        raise HTTPException(status_code=400, detail="No pipeline executed yet.")

    jobs_data = []
    for job_key, job_info in state["mapreduce_jobs"].items():
        jobs_data.append({
            "job_key": job_key,
            "job_name": job_info["job_name"],
            "execution_mode": job_info["execution_mode"],
            "status": job_info["status"],
            "duration_ms": job_info["duration_ms"],
            "metrics": job_info["metrics"],
            "output_file": job_info["output_file"],
            "sample_output": job_info["sample_output"],
            "total_results": len(job_info["parsed_results"])
        })

    return {
        "dataset_name": state["dataset_name"],
        "processing_mode": state["processing_mode"],
        "total_jobs": len(jobs_data),
        "jobs": jobs_data
    }

@router.get("/source/{job_key}")
def get_mapper_reducer_source(job_key: str):
    """
    Returns the exact Python Mapper and Reducer code for college review and demonstration.
    """
    job_key_clean = job_key.lower()
    if job_key_clean not in JOB_SCRIPT_MAP:
        raise HTTPException(status_code=404, detail=f"Job {job_key} not found. Available: {list(JOB_SCRIPT_MAP.keys())}")

    mapper_file, reducer_file = JOB_SCRIPT_MAP[job_key_clean]
    mapper_path = MAPPER_DIR / mapper_file
    reducer_path = REDUCER_DIR / reducer_file

    mapper_code = mapper_path.read_text(encoding="utf-8") if mapper_path.exists() else "# Mapper script not found"
    reducer_code = reducer_path.read_text(encoding="utf-8") if reducer_path.exists() else "# Reducer script not found"

    return {
        "job_key": job_key_clean,
        "mapper_file": mapper_file,
        "reducer_file": reducer_file,
        "mapper_code": mapper_code,
        "reducer_code": reducer_code
    }
