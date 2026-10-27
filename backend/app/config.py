import os
from pathlib import Path

# Base Directories
APP_DIR = Path(__file__).resolve().parent
BACKEND_DIR = APP_DIR.parent
PROJECT_DIR = BACKEND_DIR.parent

DATA_DIR = BACKEND_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
SAMPLE_DATA_DIR = DATA_DIR / "sample"
DB_PATH = BACKEND_DIR / "socialpulse.db"

HADOOP_DIR = PROJECT_DIR / "hadoop"
MAPPER_DIR = HADOOP_DIR / "mapper"
REDUCER_DIR = HADOOP_DIR / "reducer"
HADOOP_SCRIPTS_DIR = HADOOP_DIR / "scripts"

# Ensure runtime directories exist
for directory in [DATA_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR, SAMPLE_DATA_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Application Settings
APP_NAME = "SocialPulse 360"
APP_VERSION = "1.0.0"
DESCRIPTION = "Big Data Social Media Sentiment & Trend Analytics Platform (Hadoop/MapReduce & NLP)"

DEFAULT_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]

env_origins = os.environ.get("CORS_ORIGINS", "")
if env_origins:
    CORS_ORIGINS = [o.strip() for o in env_origins.split(",") if o.strip()]
else:
    CORS_ORIGINS = DEFAULT_ORIGINS

