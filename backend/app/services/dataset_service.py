"""
Dataset Management Service.
Handles dataset cataloging, file uploads, sample dataset registration,
and validation reporting.
"""

import os
import shutil
import uuid
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional
from app.config import SAMPLE_DATA_DIR, RAW_DATA_DIR
from app.database import get_connection
from app.services.data_cleaner import data_cleaner

class DatasetService:
    def __init__(self):
        self.ensure_samples_registered()

    def ensure_samples_registered(self):
        """Ensures default sample datasets are indexed in the database."""
        conn = get_connection()
        cursor = conn.cursor()

        sample_files = list(SAMPLE_DATA_DIR.glob("*.csv")) + list(SAMPLE_DATA_DIR.glob("*.json"))
        for file_path in sample_files:
            dataset_id = f"sample_{file_path.stem}"
            cursor.execute("SELECT id FROM datasets WHERE id = ?", (dataset_id,))
            if not cursor.fetchone():
                try:
                    df, metrics = data_cleaner.load_and_validate(file_path)
                    cursor.execute("""
                    INSERT INTO datasets (
                        id, name, file_path, file_type, source_type,
                        total_rows, total_columns, missing_count, duplicate_count, created_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        dataset_id,
                        file_path.stem.replace("_", " ").title(),
                        str(file_path),
                        file_path.suffix.lstrip(".").upper(),
                        "Sample Dataset",
                        metrics["total_rows"],
                        metrics["total_columns"],
                        metrics["missing_count"],
                        metrics["duplicate_count"],
                        datetime.now().isoformat()
                    ))
                except Exception as e:
                    print(f"Error registering sample dataset {file_path}: {e}")

        conn.commit()
        conn.close()

    def list_datasets(self) -> List[Dict[str, Any]]:
        """Returns all registered datasets with metadata."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM datasets ORDER BY created_at DESC")
        rows = cursor.fetchall()
        datasets = [dict(row) for row in rows]
        conn.close()
        return datasets

    def get_dataset(self, dataset_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves single dataset metadata by ID."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM datasets WHERE id = ?", (dataset_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    def register_uploaded_file(self, temp_path: Path, filename: str) -> Dict[str, Any]:
        """Validates and registers user-uploaded dataset."""
        file_ext = Path(filename).suffix.lower()
        if file_ext not in [".csv", ".json"]:
            raise ValueError("Only CSV and JSON formats are supported.")

        dataset_id = f"upload_{uuid.uuid4().hex[:10]}"
        dest_path = RAW_DATA_DIR / f"{dataset_id}_{filename}"
        shutil.move(str(temp_path), str(dest_path))

        # Validate
        df, metrics = data_cleaner.load_and_validate(dest_path)

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO datasets (
            id, name, file_path, file_type, source_type,
            total_rows, total_columns, missing_count, duplicate_count, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            dataset_id,
            filename,
            str(dest_path),
            file_ext.lstrip(".").upper(),
            "User Upload",
            metrics["total_rows"],
            metrics["total_columns"],
            metrics["missing_count"],
            metrics["duplicate_count"],
            datetime.now().isoformat()
        ))
        conn.commit()
        conn.close()

        return {
            "id": dataset_id,
            "name": filename,
            "file_type": file_ext.lstrip(".").upper(),
            "metrics": metrics
        }

dataset_service = DatasetService()
