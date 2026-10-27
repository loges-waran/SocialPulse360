"""
Data Cleaning and Preprocessing Service for SocialPulse 360.
Handles CSV and JSON datasets, detects schema, cleans noisy social text,
handles missing values and duplicates, and prepares records for MapReduce.
"""

import os
import json
import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple, List
from pathlib import Path
from app.utils.text_utils import clean_text, extract_hashtags, detect_language
from app.sentiment.engine import sentiment_engine

# Candidate column names for auto-detection
TEXT_CANDIDATES = ["text", "tweet", "content", "post", "message", "comment", "status", "clean_text", "sentence"]
TIMESTAMP_CANDIDATES = ["timestamp", "date", "created_at", "time", "datetime", "posted_at"]
HASHTAG_CANDIDATES = ["hashtags", "tags", "hashtag", "tag"]
AUTHOR_CANDIDATES = ["author", "user", "username", "screen_name", "handle", "sender"]
SENTIMENT_CANDIDATES = ["sentiment", "label", "polarity", "target"]

class DataCleaner:
    def detect_columns(self, df: pd.DataFrame) -> Dict[str, str]:
        """Detect standard semantic columns from arbitrary dataset."""
        detected = {}
        cols_lower = {col.lower(): col for col in df.columns}

        # Text column (Mandatory)
        for cand in TEXT_CANDIDATES:
            if cand in cols_lower:
                detected["text"] = cols_lower[cand]
                break
        if "text" not in detected:
            # Fallback: choose the column with highest average string length
            str_cols = df.select_dtypes(include=['object', 'string']).columns
            if len(str_cols) > 0:
                avg_lens = {col: df[col].astype(str).str.len().mean() for col in str_cols}
                detected["text"] = max(avg_lens, key=avg_lens.get)
            else:
                detected["text"] = df.columns[0]

        # Timestamp column
        for cand in TIMESTAMP_CANDIDATES:
            if cand in cols_lower:
                detected["timestamp"] = cols_lower[cand]
                break

        # Hashtags column
        for cand in HASHTAG_CANDIDATES:
            if cand in cols_lower:
                detected["hashtags"] = cols_lower[cand]
                break

        # Author column
        for cand in AUTHOR_CANDIDATES:
            if cand in cols_lower:
                detected["author"] = cols_lower[cand]
                break

        # Sentiment column if dataset was pre-labeled
        for cand in SENTIMENT_CANDIDATES:
            if cand in cols_lower:
                detected["sentiment"] = cols_lower[cand]
                break

        return detected

    def load_and_validate(self, file_path: Path) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Loads CSV or JSON file, gathers raw validation metrics (rows, cols, nulls, duplicates).
        """
        file_ext = file_path.suffix.lower()
        if file_ext == '.csv':
            df = pd.read_csv(file_path, encoding='utf-8', on_bad_lines='skip')
        elif file_ext in ('.json', '.jsonl'):
            try:
                df = pd.read_json(file_path, encoding='utf-8')
            except ValueError:
                # Try lines=True for JSON lines
                df = pd.read_json(file_path, lines=True, encoding='utf-8')
        else:
            raise ValueError(f"Unsupported file format: {file_ext}. Use CSV or JSON.")

        total_rows = len(df)
        total_cols = len(df.columns)
        missing_count = int(df.isnull().sum().sum())
        duplicate_count = int(df.duplicated().sum())

        col_mapping = self.detect_columns(df)

        metrics = {
            "total_rows": total_rows,
            "total_columns": total_cols,
            "missing_count": missing_count,
            "duplicate_count": duplicate_count,
            "detected_columns": col_mapping,
            "column_names": list(df.columns)
        }

        return df, metrics

    def process_and_enrich(self, df: pd.DataFrame, col_mapping: Dict[str, str]) -> pd.DataFrame:
        """
        Cleans data, removes duplicates, handles nulls, enriches with:
        - original_text
        - cleaned_text
        - language
        - sentiment
        - sentiment_score
        - sentiment_confidence
        - extracted hashtags
        """
        text_col = col_mapping["text"]
        
        # Drop duplicates based on text
        df_clean = df.dropna(subset=[text_col]).copy()
        df_clean = df_clean.drop_duplicates(subset=[text_col]).copy()

        # Handle text column
        df_clean["original_text"] = df_clean[text_col].astype(str)
        df_clean["cleaned_text"] = df_clean["original_text"].apply(
            lambda t: clean_text(t, remove_stopwords=False, keep_hashtags=False)
        )

        # Handle hashtags
        if "hashtags" in col_mapping and col_mapping["hashtags"] in df_clean.columns:
            # If hashtags exists, normalize
            def parse_tags(val):
                if pd.isna(val):
                    return []
                if isinstance(val, list):
                    return [f"#{t.strip().lstrip('#').lower()}" for t in val if t]
                return [f"#{t.strip().lstrip('#').lower()}" for t in str(val).split() if t]
            df_clean["extracted_hashtags"] = df_clean[col_mapping["hashtags"]].apply(parse_tags)
        else:
            # Extract hashtags from original text
            df_clean["extracted_hashtags"] = df_clean["original_text"].apply(
                lambda t: [f"#{h}" for h in extract_hashtags(t)]
            )

        # Handle timestamps
        if "timestamp" in col_mapping and col_mapping["timestamp"] in df_clean.columns:
            # Coerce to ISO datetime string
            df_clean["formatted_date"] = pd.to_datetime(
                df_clean[col_mapping["timestamp"]], errors='coerce'
            ).dt.strftime('%Y-%m-%d')
            # Fill missing dates with today
            df_clean["formatted_date"] = df_clean["formatted_date"].fillna(
                pd.Timestamp.now().strftime('%Y-%m-%d')
            )
        else:
            df_clean["formatted_date"] = pd.Timestamp.now().strftime('%Y-%m-%d')

        # Run NLP Sentiment Engine for each record
        sentiments = []
        scores = []
        confidences = []
        languages = []
        matched_tokens_list = []

        for text in df_clean["original_text"]:
            analysis = sentiment_engine.analyze(text)
            sentiments.append(analysis["sentiment"])
            scores.append(analysis["score"])
            confidences.append(analysis["confidence"])
            languages.append(analysis["language"])
            matched_tokens_list.append(json.dumps(analysis["matched_tokens"]))

        df_clean["sentiment"] = sentiments
        df_clean["sentiment_score"] = scores
        df_clean["sentiment_confidence"] = confidences
        df_clean["language"] = languages
        df_clean["sentiment_tokens"] = matched_tokens_list

        # Assign unique id if not present
        if "id" not in df_clean.columns:
            df_clean["id"] = range(1, len(df_clean) + 1)

        return df_clean

data_cleaner = DataCleaner()
