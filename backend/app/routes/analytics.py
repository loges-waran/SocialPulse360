"""
Analytics & Visualizations API Routes.
"""

from typing import Optional
from fastapi import APIRouter, Query, HTTPException
from app.services.pipeline_runner import pipeline_runner

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])

@router.get("/overview")
def get_analytics_overview():
    """Returns top-level KPIs for dashboard cards."""
    state = pipeline_runner.get_active_state()
    if not state:
        raise HTTPException(status_code=400, detail="No dataset has been analyzed yet.")

    dist = state["sentiment_distribution"]
    return {
        "dataset_name": state["dataset_name"],
        "dataset_id": state["dataset_id"],
        "processing_mode": state["processing_mode"],
        "total_records": state["total_records"],
        "processing_duration_ms": state["total_duration_ms"],
        "unique_words": state["word_trends"]["total_unique_words"],
        "sentiment_percentages": dist["percentages"],
        "sentiment_counts": dist["counts"],
        "sdg_alignment": {
            "goal": "SDG 9: Industry, Innovation and Infrastructure",
            "relevance": "Monitoring social sentiment and infrastructure feedback across transport, energy, and digital connectivity."
        }
    }

@router.get("/sentiment")
def get_sentiment_analytics():
    """Returns detailed sentiment distribution and daily trends."""
    state = pipeline_runner.get_active_state()
    if not state:
        raise HTTPException(status_code=400, detail="No dataset has been analyzed yet.")

    return {
        "sentiment_distribution": state["sentiment_distribution"],
        "daily_timeline": state["daily_timeline"],
        "sentiment_keywords": state["sentiment_keywords"]
    }

@router.get("/trends")
def get_trend_analytics():
    """Returns top frequent words, top hashtags, and keyword comparison."""
    state = pipeline_runner.get_active_state()
    if not state:
        raise HTTPException(status_code=400, detail="No dataset has been analyzed yet.")

    return {
        "word_trends": state["word_trends"],
        "top_hashtags": state["top_hashtags"],
        "sentiment_keywords": state["sentiment_keywords"],
        "methodology_note": "Word frequency is calculated using Hadoop MapReduce token counting. Note: High frequency indicates prevalence in discourse but does not inherently denote semantic significance."
    }

@router.get("/word-frequency")
def get_word_frequencies(limit: int = Query(50, ge=5, le=200)):
    """Returns word frequency ranking up to specified limit."""
    state = pipeline_runner.get_active_state()
    if not state:
        raise HTTPException(status_code=400, detail="No dataset has been analyzed yet.")

    all_words = state["mapreduce_jobs"]["wordcount"]["parsed_results"]
    sorted_words = sorted(all_words, key=lambda x: x["value"], reverse=True)
    return {
        "total_unique": len(sorted_words),
        "words": sorted_words[:limit]
    }

@router.get("/records")
def get_analyzed_records(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    sentiment: Optional[str] = Query(None),
    language: Optional[str] = Query(None),
    search: Optional[str] = Query(None)
):
    """
    Returns paginated, filterable, searchable records from the processed dataset.
    """
    state = pipeline_runner.get_active_state()
    if not state:
        raise HTTPException(status_code=400, detail="No dataset has been analyzed yet.")

    records = state["records"]

    # Filter by sentiment
    if sentiment and sentiment.lower() != "all":
        records = [r for r in records if str(r.get("sentiment", "")).lower() == sentiment.lower()]

    # Filter by language
    if language and language.lower() != "all":
        records = [r for r in records if str(r.get("language", "")).lower() == language.lower()]

    # Search in text
    if search and search.strip():
        q = search.strip().lower()
        records = [
            r for r in records 
            if q in str(r.get("original_text", "")).lower() or q in str(r.get("cleaned_text", "")).lower()
        ]

    total_matched = len(records)
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    page_items = records[start_idx:end_idx]

    return {
        "page": page,
        "page_size": page_size,
        "total_records": total_matched,
        "total_pages": (total_matched + page_size - 1) // page_size if total_matched > 0 else 1,
        "records": page_items
    }
