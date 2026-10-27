<<<<<<< HEAD
# SocialPulse 360 — Social Media Sentiment & Trend Analytics

[![Big Data Analytics](https://img.shields.io/badge/Big_Data-Hadoop_MapReduce-blue.svg)](https://hadoop.apache.org/)
[![Python](https://img.shields.io/badge/Python-3.13-yellow.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/Frontend-React_18_%2B_Vite-61DAFB.svg)](https://vitejs.dev/)
[![SDG 9](https://img.shields.io/badge/SDG_9-Industry,_Innovation_%26_Infrastructure-FD6925.svg)](https://sdgs.un.org/goals/goal9)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An industry-standard Big Data Analytics (BDA) mini-project designed to analyze **Tamil-English (Tanglish)** and **English** social media discourse. Built using **Apache Hadoop, HDFS, and MapReduce** concepts, an explainable **NLP Sentiment Classifier**, a **FastAPI backend**, and a **React + Vite dark-themed analytics dashboard**.

Aligned with **United Nations Sustainable Development Goal 9 (SDG 9: Industry, Innovation, and Infrastructure)**.

---

## Table of Contents

1. [Project Overview & Objectives](#1-project-overview--objectives)
2. [Problem Statement & SDG 9 Alignment](#2-problem-statement--sdg-9-alignment)
3. [System Architecture](#3-system-architecture)
4. [Technologies Used](#4-technologies-used)
5. [Dataset Management & Tanglish Support](#5-dataset-management--tanglish-support)
6. [MapReduce Processing Pipeline](#6-mapreduce-processing-pipeline)
7. [Installation & Windows Setup Guide](#7-installation--windows-setup-guide)
8. [Running the Application](#8-running-the-application)
9. [Hadoop Cluster & HDFS Instructions](#9-hadoop-cluster--hdfs-instructions)
10. [REST API Documentation](#10-rest-api-documentation)
11. [Testing & Verification](#11-testing--verification)
12. [Limitations & Future Enhancements](#12-limitations--future-enhancements)
13. [GitHub Upload Instructions](#13-github-upload-instructions)

---

## 1. Project Overview & Objectives

**SocialPulse 360** transforms social media streams into structured sentiment and trend intelligence. It answers critical questions:
- What is the breakdown of **positive, negative, and neutral** sentiment across public posts?
- What are the **top trending words** and **viral hashtags**?
- How does citizen sentiment **change across dates**?
- Which specific expressions are associated with **positive praise** versus **negative grievances**?
- How can distributed **Hadoop MapReduce** algorithms process unstructured social data at scale?

---

## 2. Problem Statement & SDG 9 Alignment

### Problem Statement
Standard social analytics tools either require expensive commercial cloud licenses or are strictly English-centric. In multilingual hubs like Tamil Nadu, citizens communicate extensively in **Tanglish** (phonetic Tamil written using Latin English characters, e.g., *"Intha movie semma mass ah irukku"*, *"Service romba waste and mokka"*). Existing tools fail to recognize these emotional indicators. Furthermore, academic projects often discuss Hadoop theoretically without actual verifiable MapReduce implementations.

### SDG 9 Alignment: Industry, Innovation, and Infrastructure
SocialPulse 360 is mapped directly to **SDG Target 9.1 & 9.c**:
- **Target 9.1 (Resilient Infrastructure):** Monitors public sentiment regarding mass transit systems (Chennai Metro CMRL, Southern Railways), highway corridors (OMR, NHAI), and public utilities to detect infrastructure bottlenecks.
- **Target 9.c (Universal ICT Access):** Identifies regional telecom outages, broadband disruptions, and 5G network rollouts from citizen tweets.
- **Target 9.5 (Technological Capabilities):** Delivers an open, transparent, explainable NLP engine for low-resource code-mixed languages.

---

## 3. System Architecture

```
Data Ingestion (CSV / JSON)
        ↓
Data Validation & Cleaning (Auto-detect schema, drop duplicates, handle nulls)
        ↓
Hybrid NLP Sentiment Engine (English + Tanglish transliterated lexicon)
        ↓
Staging Area (Formatted streaming TSVs)
        ↓
MapReduce Processing (5 Distinct Jobs: Mapper → Shuffle/Sort → Reducer)
        ↓
Trend Aggregation & SQLite Catalog
        ↓
FastAPI Backend (/api/analytics, /api/mapreduce, /api/export)
        ↓
Interactive React + Vite Dashboard
```

---

## 4. Technologies Used

- **Distributed Big Data Core:** Apache Hadoop, HDFS, Hadoop Streaming
- **MapReduce Implementation:** Python 3 (`stdin` / `stdout` pipes) + Local MapReduce Simulation Framework
- **Backend Framework:** FastAPI, Uvicorn, Pydantic, SQLite
- **Data Engineering:** Pandas, NumPy
- **NLP & Sentiment Analysis:** Custom Tanglish & Tamil Valence Lexicon + English VADER/AFINN-style booster engine
- **Frontend Framework:** React 18, Vite, Tailwind CSS, Lucide React
- **Data Visualizations:** Recharts (Donut charts, Bar charts, Area timeline charts, Progress bars)
- **Quality Assurance:** Pytest (18 unit & integration tests)

---

## 5. Dataset Management & Tanglish Support

### Bundled Datasets
- `backend/data/sample/sample_social_tanglish_english.csv`: 48 rich posts covering tech infrastructure, Chennai Metro, OMR traffic, telecom outages, cinema, and solar energy in English, Tanglish, and Tamil.
- `backend/data/sample/sample_social_tweets.json`: Equivalent structured JSON format.

### Uploading Custom Datasets
Users can upload any CSV or JSON file through the UI or via `POST /api/datasets/upload`. The system automatically:
- Detects the text, timestamp, hashtags, author, and sentiment columns.
- Removes duplicates and handles missing values.
- Preserves the `original_text` while creating a normalized `cleaned_text` field.

### Tanglish Sentiment Lexicon
The engine recognizes characteristic Tanglish tokens:
- **Positive:** *semma (+3.4), mass (+3.2), vera level (+3.8), tharumaru (+3.5), super (+2.8), nalla (+2.2), azhagu (+2.5), magizhchi (+3.0), perumai (+3.0), vetri (+3.0)*
- **Negative:** *mokka (-3.2), waste (-3.0), karumam (-3.6), mosam (-3.2), kevalam (-3.5), kodumai (-3.4), kashtam (-2.6), tholvi (-3.0), cringe (-2.8)*
- **Intensifiers & Boosters:** *romba, semmaya, bayangara, migavum*
- **Negators:** *illa, illatha, mudiyala, kedaikala, maatudhu*

---

## 6. MapReduce Processing Pipeline

SocialPulse 360 provides 5 separate MapReduce jobs in `hadoop/mapper/` and `hadoop/reducer/`:

| Job Name | Mapper Script | Reducer Script | Emitted Key-Value Contract |
| :--- | :--- | :--- | :--- |
| **1. WordCount** | `wordcount_mapper.py` | `wordcount_reducer.py` | `word\t1` $\rightarrow$ `word\ttotal_count` |
| **2. HashtagCount** | `hashtag_mapper.py` | `hashtag_reducer.py` | `#tag\t1` $\rightarrow$ `#tag\ttotal_count` |
| **3. SentimentAgg** | `sentiment_mapper.py` | `sentiment_reducer.py` | `sentiment\t1` $\rightarrow$ `sentiment\ttotal_count` |
| **4. DailySentiment** | `daily_sentiment_mapper.py` | `daily_sentiment_reducer.py` | `YYYY-MM-DD:sentiment\t1` $\rightarrow$ `count` |
| **5. SentimentWords** | `sentiment_words_mapper.py` | `sentiment_words_reducer.py` | `sentiment:word\t1` $\rightarrow$ `count` |

---

## 7. Installation & Windows Setup Guide

### Prerequisites
- **Python 3.10+** (Tested on Python 3.13)
- **Node.js 18+** (Tested on Node.js v24.20.0)
- **Git**

### Step-by-Step Installation

```powershell
# 1. Clone the repository
git clone https://github.com/your-username/SocialPulse360.git
cd SocialPulse360

# 2. Install Backend Python Dependencies
cd backend
pip install -r requirements.txt

# 3. Install Frontend Dependencies
cd ../frontend
npm install
```

---

## 8. Running the Application

### Option A: One-Click Startup (Windows)
Double-click `scripts/run_all.bat` or run:
```powershell
.\scripts\run_all.bat
```
This automatically launches both backend and frontend in separate terminal windows.

### Option B: Manual Startup

**Terminal 1 — Backend:**
```powershell
cd backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
API runs at: `http://127.0.0.1:8000`  
Interactive Swagger Docs: `http://127.0.0.1:8000/docs`

**Terminal 2 — Frontend:**
```powershell
cd frontend
npm run dev
```
Dashboard opens at: `http://localhost:5173`

---

## 9. Hadoop Cluster & HDFS Instructions

If you have Apache Hadoop installed, execute the jobs directly on your Hadoop cluster:

### 1. Initialize HDFS Directories
```bash
bash hadoop/scripts/hdfs_setup.sh
# Or on Windows:
hadoop\scripts\hdfs_setup.bat
```

### 2. Run Hadoop Streaming Jobs
```bash
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
  -files hadoop/mapper/wordcount_mapper.py,hadoop/reducer/wordcount_reducer.py \
  -mapper "python3 wordcount_mapper.py" \
  -reducer "python3 wordcount_reducer.py" \
  -input /socialpulse/input \
  -output /socialpulse/output/wordcount
```

### 3. Local Standalone Simulation (Offline Mode)
On machines without Hadoop installed, run the standalone simulation:
```powershell
cd hadoop/scripts
python run_local_simulation.py --job wordcount
python run_local_simulation.py --job hashtag
python run_local_simulation.py --job sentiment
python run_local_simulation.py --job daily
python run_local_simulation.py --job sentiment_words
```

---

## 10. REST API Documentation

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/api/health` | `GET` | Health check and engine capabilities |
| `/api/datasets` | `GET` | List all available sample and uploaded datasets |
| `/api/datasets/upload` | `POST` | Upload a new CSV or JSON dataset |
| `/api/analysis/run` | `POST` | Execute the Big Data pipeline on a dataset |
| `/api/analytics/overview` | `GET` | Top-level KPIs and summary metrics |
| `/api/analytics/sentiment` | `GET` | Sentiment percentages, counts, and daily timeline |
| `/api/analytics/trends` | `GET` | Top words (10/20/50), hashtags, and keyword comparison |
| `/api/analytics/records` | `GET` | Searchable, paginated dataset records with sentiment |
| `/api/mapreduce/jobs` | `GET` | Telemetry for all 5 executed MapReduce jobs |
| `/api/mapreduce/source/{job}` | `GET` | Inspect Python Mapper & Reducer source code |
| `/api/export/csv` | `GET` | Download enriched dataset as CSV |

---

## 11. Testing & Verification

Run the automated backend test suite:
```powershell
cd backend
python -m pytest -v
```
**Results:** `18 passed in 8.22s`
- Verified: Text cleaning, hashtag extraction, language detection, tokenization.
- Verified: English and Tanglish positive, negative, and neutral sentiment classification.
- Verified: Subprocess MapReduce execution, sort/shuffle phase, and reducer counts.
- Verified: FastAPI health, datasets, analytics overview, and records pagination.

Verify frontend build:
```powershell
cd frontend
npm run build
```
**Result:** `✓ built in 13.85s` with 0 errors.

---

## 12. Limitations & Future Enhancements

### Limitations
- Sarcasm detection in Tanglish is limited when contextual world knowledge is required.
- Real-world social APIs (e.g., Twitter/X API) require paid developer credentials; thus, dataset upload and streaming file ingestion are prioritized.

### Future Enhancements
- Integration with **Apache Spark Streaming** and **Kafka** for sub-second live tweet processing.
- Fine-tuned transformer models (e.g., IndicBERT) for deep morphological Tamil disambiguation.
- Geospatial mapping to highlight infrastructure complaints on OpenStreetMap.

---

## 13. GitHub Upload Instructions

```powershell
git init
git add .
git commit -m "feat: complete SocialPulse 360 Big Data Analytics project"
git branch -M main
git remote add origin https://github.com/your-username/SocialPulse360.git
git push -u origin main
```

---

## License

This project is licensed under the [MIT License](LICENSE).
=======
# SocialPulse 360

**Social Media Sentiment and Trend Analytics**

SocialPulse 360 is a dashboard project that analyzes Tamil-English social media text using sentiment categories and word-frequency analysis.

## Features

- Sentiment analysis summary
- Search social media text by word or phrase
- Word-frequency and trend analytics
- Interactive Streamlit dashboard
- Apache Hadoop MapReduce word-count processing

## Technology Stack

- Python
- Streamlit
- Pandas
- Apache Hadoop
- MapReduce

## Dataset

The project uses a cleaned Tamil-English social media text dataset containing 15,601 records.

The dataset is not included in this repository. Add the dataset locally before running the application.

## Run Locally

1. Install Python and Apache Hadoop.
2. Install the required Python packages.
3. Configure the dataset path in `app.py`.
4. Start the dashboard:

```bash
streamlit run app.py
>>>>>>> 6f2a9c26f5f9223822b36825a40c9432cdfefaad
