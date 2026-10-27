"""
SocialPulse 360 - Main FastAPI Backend Application.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import APP_NAME, APP_VERSION, DESCRIPTION, CORS_ORIGINS
from app.routes import datasets, analysis, analytics, mapreduce_routes, export

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description=DESCRIPTION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_origin_regex=r"^https?://.*\.vercel\.app$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(datasets.router)
app.include_router(analysis.router)
app.include_router(analytics.router)
app.include_router(mapreduce_routes.router)
app.include_router(export.router)

@app.get("/api/health", tags=["Health"])
def health_check():
    """Health check endpoint indicating backend operational status."""
    return {
        "status": "UP",
        "service": APP_NAME,
        "version": APP_VERSION,
        "features": {
            "hadoop_mapreduce": "Local Simulation & Hadoop Streaming compatible",
            "nlp_sentiment": "English, Tanglish, and Tamil supported",
            "dataset_formats": ["CSV", "JSON"],
            "sdg_alignment": "SDG 9 Industry, Innovation & Infrastructure"
        }
    }

@app.get("/", tags=["Root"])
def root():
    return {
        "message": f"Welcome to {APP_NAME} Backend API",
        "documentation": "/docs",
        "health": "/api/health"
    }

if __name__ == "__main__":
    import os
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")
    uvicorn.run("app.main:app", host=host, port=port, reload=False)
