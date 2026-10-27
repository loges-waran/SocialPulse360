"""
Pipeline Runner Service.
Orchestrates the entire Big Data Processing Pipeline:
Data Validation -> Data Cleaning -> Staging -> MapReduce Execution -> Trend Aggregation -> Persistence.
"""

import time
import json
import uuid
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional
import pandas as pd

from app.config import PROCESSED_DATA_DIR
from app.database import get_connection
from app.services.data_cleaner import data_cleaner
from app.services.dataset_service import dataset_service
from app.mapreduce.local_runner import local_mr_runner
from app.analytics.trend_analyzer import trend_analyzer

class PipelineRunner:
    def __init__(self):
        # In-memory store for currently active analyzed dataset
        self.active_pipeline_state: Optional[Dict[str, Any]] = None

    def execute_pipeline(self, dataset_id: str, processing_mode: str = "local") -> Dict[str, Any]:
        """
        Executes end-to-end Big Data pipeline for given dataset ID.
        """
        job_id = f"job_{uuid.uuid4().hex[:12]}"
        start_overall = time.perf_counter()

        # Step 1: Ingest & Validate
        ds_meta = dataset_service.get_dataset(dataset_id)
        if not ds_meta:
            raise ValueError(f"Dataset {dataset_id} not found.")

        file_path = Path(ds_meta["file_path"])
        df_raw, validation_metrics = data_cleaner.load_and_validate(file_path)

        # Step 2: Clean & Enrich (NLP Sentiment Inference)
        df_enriched = data_cleaner.process_and_enrich(df_raw, validation_metrics["detected_columns"])

        # Save processed dataset
        processed_file_path = PROCESSED_DATA_DIR / f"{dataset_id}_processed.csv"
        df_enriched.to_csv(processed_file_path, index=False, encoding='utf-8')

        # Step 3: Prepare Stage Inputs for MapReduce Jobs
        # Input 1: Text stream for WordCount
        wordcount_input = "\n".join(df_enriched["cleaned_text"].tolist())

        # Input 2: Text stream for Hashtag Count (original text preserves #)
        hashtag_input = "\n".join(df_enriched["original_text"].tolist())

        # Input 3: Sentiment stream for Sentiment Aggregation
        sentiment_input = "\n".join([f"id_{i}\t{s}" for i, s in enumerate(df_enriched["sentiment"])])

        # Input 4: Daily sentiment stream
        daily_input = "\n".join([
            f"{row['formatted_date']}\t{row['sentiment']}" 
            for _, row in df_enriched.iterrows()
        ])

        # Input 5: Sentiment words stream
        sentiment_words_input = "\n".join([
            f"{row['sentiment']}\t{row['cleaned_text']}" 
            for _, row in df_enriched.iterrows()
        ])

        # Step 4: Execute 5 MapReduce Jobs
        mr_jobs = {}
        
        # 1. Word Count
        mr_jobs["wordcount"] = local_mr_runner.run_job(
            "WordCount", "wordcount_mapper.py", "wordcount_reducer.py", wordcount_input
        )
        
        # 2. Hashtag Count
        mr_jobs["hashtags"] = local_mr_runner.run_job(
            "HashtagCount", "hashtag_mapper.py", "hashtag_reducer.py", hashtag_input
        )

        # 3. Sentiment Aggregation
        mr_jobs["sentiment"] = local_mr_runner.run_job(
            "SentimentAgg", "sentiment_mapper.py", "sentiment_reducer.py", sentiment_input
        )

        # 4. Daily Sentiment
        mr_jobs["daily"] = local_mr_runner.run_job(
            "DailySentiment", "daily_sentiment_mapper.py", "daily_sentiment_reducer.py", daily_input
        )

        # 5. Sentiment Words
        mr_jobs["sentiment_words"] = local_mr_runner.run_job(
            "SentimentWords", "sentiment_words_mapper.py", "sentiment_words_reducer.py", sentiment_words_input
        )

        # Step 5: Analytics and Trend Aggregation
        sentiment_dist = trend_analyzer.calculate_sentiment_distribution(mr_jobs["sentiment"]["parsed_results"])
        word_trends = trend_analyzer.aggregate_word_trends(mr_jobs["wordcount"]["parsed_results"])
        top_hashtags = trend_analyzer.aggregate_hashtags(mr_jobs["hashtags"]["parsed_results"])
        sentiment_keywords = trend_analyzer.aggregate_sentiment_words(mr_jobs["sentiment_words"]["parsed_results"])
        daily_timeline = trend_analyzer.aggregate_daily_trends(mr_jobs["daily"]["parsed_results"])

        total_duration_ms = round((time.perf_counter() - start_overall) * 1000, 2)

        # Step 6: Persist Job to SQLite
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO jobs (
            id, dataset_id, status, processing_mode, total_records, duration_ms,
            positive_count, negative_count, neutral_count, unique_words, metrics_json, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            job_id,
            dataset_id,
            "SUCCESS",
            "Local MapReduce (Hadoop Engine)",
            len(df_enriched),
            total_duration_ms,
            sentiment_dist["counts"].get("positive", 0),
            sentiment_dist["counts"].get("negative", 0),
            sentiment_dist["counts"].get("neutral", 0),
            word_trends["total_unique_words"],
            json.dumps({
                "mr_jobs_summary": {k: v["metrics"] for k, v in mr_jobs.items()},
                "validation": validation_metrics
            }),
            datetime.now().isoformat()
        ))
        conn.commit()
        conn.close()

        # Step 7: Store active pipeline state
        pipeline_output = {
            "job_id": job_id,
            "dataset_id": dataset_id,
            "dataset_name": ds_meta["name"],
            "processing_mode": "Local MapReduce (Hadoop Emulation)" if processing_mode == "local" else "Hadoop Cluster",
            "total_records": len(df_enriched),
            "total_duration_ms": total_duration_ms,
            "validation_metrics": validation_metrics,
            "sentiment_distribution": sentiment_dist,
            "word_trends": word_trends,
            "top_hashtags": top_hashtags,
            "sentiment_keywords": sentiment_keywords,
            "daily_timeline": daily_timeline,
            "mapreduce_jobs": mr_jobs,
            "processed_file_path": str(processed_file_path),
            "records": df_enriched.to_dict(orient="records")
        }

        self.active_pipeline_state = pipeline_output
        return pipeline_output

    def get_active_state(self) -> Optional[Dict[str, Any]]:
        """Return currently cached active pipeline results or initialize from sample if empty."""
        if not self.active_pipeline_state:
            # Auto-run sample dataset
            sample_datasets = dataset_service.list_datasets()
            if sample_datasets:
                self.execute_pipeline(sample_datasets[0]["id"])
        return self.active_pipeline_state

pipeline_runner = PipelineRunner()
