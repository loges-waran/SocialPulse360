"""
CSV Export API Route.
"""

from pathlib import Path
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from app.services.pipeline_runner import pipeline_runner

router = APIRouter(prefix="/api/export", tags=["Export"])

@router.get("/csv")
def export_processed_csv():
    """
    Downloads the enriched analytics dataset containing original text,
    cleaned text, sentiment classifications, scores, confidences, and language tags.
    """
    state = pipeline_runner.get_active_state()
    if not state or "processed_file_path" not in state:
        raise HTTPException(status_code=400, detail="No processed dataset ready for export.")

    file_path = Path(state["processed_file_path"])
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Export file not found on disk.")

    return FileResponse(
        path=str(file_path),
        filename=f"SocialPulse360_{state['dataset_id']}_analyzed.csv",
        media_type="text/csv"
    )
