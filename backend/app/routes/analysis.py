"""
Analysis and Pipeline Execution API Routes.
"""

from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from typing import Optional
from app.services.pipeline_runner import pipeline_runner
from app.database import get_connection

router = APIRouter(prefix="/api/analysis", tags=["Analysis"])

class RunAnalysisRequest(BaseModel):
    dataset_id: str
    processing_mode: Optional[str] = "local"

@router.post("/run")
def run_analysis(request: RunAnalysisRequest):
    """
    Executes the Big Data Processing Pipeline on the specified dataset:
    Validation -> Cleaning -> NLP Sentiment -> 5 MapReduce Jobs -> Analytics.
    """
    try:
        results = pipeline_runner.execute_pipeline(
            dataset_id=request.dataset_id,
            processing_mode=request.processing_mode
        )
        return {
            "status": "COMPLETED",
            "message": "Big Data pipeline executed successfully",
            "job_id": results["job_id"],
            "dataset_name": results["dataset_name"],
            "total_records": results["total_records"],
            "duration_ms": results["total_duration_ms"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status/{job_id}")
def get_job_status(job_id: str):
    """Retrieves status and high-level metrics of an executed pipeline job."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM jobs WHERE id = ?", (job_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Job not found")

    return {"job": dict(row)}
