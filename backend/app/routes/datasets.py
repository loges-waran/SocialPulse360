"""
Dataset API Routes.
"""

import os
import shutil
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.dataset_service import dataset_service

router = APIRouter(prefix="/api/datasets", tags=["Datasets"])

@router.get("")
def list_all_datasets():
    """Lists all registered sample and uploaded datasets."""
    datasets = dataset_service.list_datasets()
    return {"datasets": datasets}

@router.get("/{dataset_id}")
def get_dataset_details(dataset_id: str):
    """Retrieves metadata and validation stats for a specific dataset."""
    dataset = dataset_service.get_dataset(dataset_id)
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return {"dataset": dataset}

@router.post("/upload")
async def upload_dataset(file: UploadFile = File(...)):
    """Uploads a CSV or JSON dataset for processing."""
    if not file.filename.lower().endswith(('.csv', '.json')):
        raise HTTPException(status_code=400, detail="Invalid format. Only CSV and JSON files are supported.")

    temp_path = Path(f"temp_{file.filename}")
    try:
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        result = dataset_service.register_uploaded_file(temp_path, file.filename)
        return {
            "message": "Dataset uploaded and registered successfully",
            "dataset": result
        }
    except Exception as e:
        if temp_path.exists():
            temp_path.unlink()
        raise HTTPException(status_code=400, detail=str(e))
