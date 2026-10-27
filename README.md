# SocialPulse 360 — Social Media Sentiment & Trend Analytics

[![Live Demo](https://img.shields.io/badge/Live_Dashboard-social--pulse360.vercel.app-00dfa2?style=for-the-badge&logo=vercel&logoColor=white)](https://social-pulse360.vercel.app/)
[![API Status](https://img.shields.io/badge/Backend_API-socialpulse360.onrender.com-46E3B7?style=for-the-badge&logo=render&logoColor=white)](https://socialpulse360.onrender.com/docs)

[![Big Data Analytics](https://img.shields.io/badge/Big_Data-Hadoop_MapReduce-blue.svg)](https://hadoop.apache.org/)
[![Python](https://img.shields.io/badge/Python-3.13-yellow.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/Frontend-React_18_%2B_Vite-61DAFB.svg)](https://vitejs.dev/)
[![SDG 9](https://img.shields.io/badge/SDG_9-Industry,_Innovation_%26_Infrastructure-FD6925.svg)](https://sdgs.un.org/goals/goal9)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> 🌐 **Live Public Dashboard:** [https://social-pulse360.vercel.app/](https://social-pulse360.vercel.app/)  
> ⚡ **Interactive API Swagger Docs:** [https://socialpulse360.onrender.com/docs](https://socialpulse360.onrender.com/docs)  
> 🏥 **Backend Health Check:** [https://socialpulse360.onrender.com/api/health](https://socialpulse360.onrender.com/api/health)

An industry-standard Big Data Analytics (BDA) platform designed to analyze **Tamil-English (Tanglish)** and **English** social media discourse. Built using **Apache Hadoop, HDFS, and MapReduce** concepts, an explainable **NLP Sentiment Classifier**, a **FastAPI backend**, and a modern **React + Vite dark-themed analytics dashboard**.

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
8. [Running the Application Locally](#8-running-the-application-locally)
9. [Production Deployment Guide (Vercel & Render)](#9-production-deployment-guide-vercel--render)
10. [Hadoop Cluster & HDFS Instructions](#10-hadoop-cluster--hdfs-instructions)
11. [REST API Documentation](#11-rest-api-documentation)
12. [Testing & Verification](#12-testing--verification)
13. [Limitations & Future Enhancements](#13-limitations--future-enhancements)
14. [License](#license)

---

## 1. Project Overview & Objectives

**SocialPulse 360** transforms social media streams into structured sentiment and trend intelligence:
- Quantifies **positive, negative, and neutral** sentiment distributions.
- Extracts **top trending words** and **viral hashtags**.
- Tracks **daily sentiment shifts** over time via timeline curves.
- Identifies specific expressions associated with **praise vs. infrastructure grievances**.
- Demonstrates distributed **Hadoop MapReduce** execution with verified telemetry.

---

## 2. Problem Statement & SDG 9 Alignment

### Problem Statement
Standard social analytics tools are largely English-centric and fail on regional code-mixed dialects. In Tamil Nadu and the broader diaspora, millions communicate in **Tanglish** (phonetic Tamil written using Latin script, e.g., *"Intha movie semma mass ah irukku"*, *"Worst customer service romba waste"*). Furthermore, academic projects often discuss Big Data conceptually without actual working MapReduce jobs.

### SDG 9 Alignment: Industry, Innovation, and Infrastructure
SocialPulse 360 is mapped directly to **UN SDG Target 9.1 & 9.c**:
- **Target 9.1 (Resilient Infrastructure):** Monitors citizen feedback on public transit (Chennai Metro CMRL, Southern Railways), road congestion (OMR, NHAI), and power grids.
- **Target 9.c (Universal ICT Access):** Tracks citizen discourse on telecom outages, broadband downtime, and 5G network rollouts.
- **Target 9.5 (Technological Capabilities):** Delivers an open, transparent, explainable NLP engine for low-resource code-mixed languages.

---

## 3. System Architecture

```
Social Media Ingestion (CSV / JSON)
        ↓
Data Validation & Cleaning (Auto-detect schema, drop duplicates, handle missing values)
        ↓
Hybrid NLP Sentiment Classifier (English + Tanglish transliterated lexicon & boosters)
        ↓
HDFS / Local Staging Data Layer (/socialpulse/input/)
        ↓
Hadoop MapReduce Processing (5 Distinct Jobs: Mapper → Sort & Shuffle → Reducer)
        ↓
Trend Aggregation & SQLite Catalog
        ↓
FastAPI Backend API (/docs interactive Swagger UI)
        ↓
React + Vite Dark Analytics Dashboard (Recharts + Tailwind CSS)
```

---

## 4. Technologies Used

- **Distributed Big Data Core:** Apache Hadoop, HDFS, Hadoop Streaming
- **MapReduce Implementation:** Python 3 (`stdin` / `stdout` pipes) + Local MapReduce Simulation Framework
- **Backend Framework:** FastAPI, Uvicorn, Gunicorn, Pydantic, SQLite
- **Data Engineering:** Pandas, NumPy
- **NLP & Sentiment Analysis:** Custom Tanglish & Tamil Valence Lexicon + English booster engine
- **Frontend Framework:** React 18, Vite, Tailwind CSS, Lucide React
- **Data Visualizations:** Recharts (Donut, Bar, Area Timeline, Progress bars)
- **Deployment & Hosting:** Vercel (Frontend), Render / Railway (Backend)
- **Quality Assurance:** Pytest (18 unit & integration tests)

---

## 5. Dataset Management & Tanglish Support

### Bundled Datasets
1. `backend/data/sample/tamil_sentiment_clean.csv`: Full benchmark dataset containing **15,601 Tamil & Tanglish social posts**.
2. `backend/data/sample/sample_social_tanglish_english.csv`: 48 rich posts covering tech infrastructure, Chennai Metro, OMR traffic, telecom outages, cinema, and solar energy in English, Tanglish, and Tamil.
3. `backend/data/sample/sample_social_tweets.json`: Structured JSON format.

### Uploading Custom Datasets
Users can upload any CSV or JSON file through the UI or via `POST /api/datasets/upload`. The system automatically:
- Detects the text, timestamp, hashtags, author, and sentiment columns.
- Removes duplicates and handles missing values.
- Preserves the `original_text` while generating a normalized `cleaned_text` field.

### Tanglish Sentiment Lexicon
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

```powershell
# 1. Clone repository
git clone https://github.com/loges-waran/SocialPulse360.git
cd SocialPulse360

# 2. Install Backend Python Dependencies
cd backend
pip install -r requirements.txt

# 3. Install Frontend Dependencies
cd ../frontend
npm install
```

---

## 8. Running the Application Locally

### Option A: One-Click Startup (Windows)
Double-click `scripts/run_all.bat` or run:
```powershell
.\scripts\run_all.bat
```

### Option B: Manual Startup

**Terminal 1 — Backend:**
```powershell
cd backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
- API: `http://127.0.0.1:8000`
- Interactive Swagger Docs: `http://127.0.0.1:8000/docs`

**Terminal 2 — Frontend:**
```powershell
cd frontend
npm run dev
```
- Dashboard: `http://localhost:5173`

---

## 9. Production Deployment Guide (Vercel & Render)

The project is deployed and live at the following public endpoints:

| Service | Hosting Platform | Live URL |
| :--- | :--- | :--- |
| **Frontend Web Dashboard** | **Vercel** | [https://social-pulse360.vercel.app/](https://social-pulse360.vercel.app/) |
| **Backend API & Swagger Docs** | **Render** | [https://socialpulse360.onrender.com/docs](https://socialpulse360.onrender.com/docs) |
| **Backend Health Check** | **Render** | [https://socialpulse360.onrender.com/api/health](https://socialpulse360.onrender.com/api/health) |

```
                      User's Web Browser
                             │
            ┌────────────────┴────────────────┐
            ▼                                 ▼
   [Vercel Public URL]               [Render Public URL]
  React + Vite Frontend              FastAPI Backend API
https://social-pulse360.vercel.app   https://socialpulse360.onrender.com
```

### Part 1: Deploy Backend on Render (Python)

1. Sign up / Log in to [Render](https://render.com/).
2. Click **New +** $\rightarrow$ **Web Service**.
3. Connect your GitHub repository: `https://github.com/loges-waran/SocialPulse360`.
4. Configure the service:
   - **Name:** `socialpulse360-api` (or your choice)
   - **Region:** Any (e.g., Oregon or Frankfurt)
   - **Branch:** `master` (or `main`)
   - **Root Directory:** `backend`
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Under **Environment Variables**, add:
   - `PYTHON_VERSION` = `3.11.9`
   - `CORS_ORIGINS` = `*`
   - `HADOOP_MODE` = `local`
6. Click **Deploy Web Service**.
7. Once deployed, Render will provide a public URL (e.g. `https://socialpulse360-api.onrender.com`).
   - Verify by visiting: `https://socialpulse360-api.onrender.com/api/health`
   - Response: `{"status": "UP", "service": "SocialPulse 360", ...}`

---

### Part 2: Deploy Frontend on Vercel (React + Vite)

1. Sign up / Log in to [Vercel](https://vercel.com/).
2. Click **Add New...** $\rightarrow$ **Project**.
3. Import your GitHub repository: `https://github.com/loges-waran/SocialPulse360`.
4. In the configuration window:
   - **Root Directory:** Click Edit and select `frontend` (or leave default if using root `vercel.json`).
   - **Framework Preset:** `Vite`
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`
5. Under **Environment Variables**, add:
   - **Name:** `VITE_API_BASE`
   - **Value:** `https://socialpulse360-api.onrender.com` *(Paste your Render backend URL from Part 1, without trailing slash)*
6. Click **Deploy**.
7. Vercel will build and assign a public live URL (e.g., `https://socialpulse-360.vercel.app`).
8. Open the URL to access your live dashboard!

---

### Part 3: Do I Need to Deploy Hadoop Separately?

**No.** The platform features a dual-mode Big Data architecture:
1. **Cloud Production Mode (Render / Vercel):** Operates using the built-in **Local MapReduce Engine** (`backend/app/mapreduce/local_runner.py`). This executes the actual Python Mapper and Reducer processes via standard Unix/Windows pipes, performs real key partitioning and sorting, and generates verifiable MapReduce metrics without needing a heavy Java Hadoop cluster on Render.
2. **Cluster Mode (Optional / On-Premise):** The same mapper and reducer scripts in `hadoop/mapper/` and `hadoop/reducer/` can be submitted to an on-premise Apache Hadoop cluster using standard `hadoop-streaming.jar` commands.

---

## 10. Hadoop Cluster & HDFS Instructions

If you have Apache Hadoop installed locally or on a server, run the cluster jobs directly:

### 1. Initialize HDFS Directories
```bash
bash hadoop/scripts/hdfs_setup.sh
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

### 3. Local Standalone Simulation (CLI)
```powershell
cd hadoop/scripts
python run_local_simulation.py --job wordcount
python run_local_simulation.py --job hashtag
python run_local_simulation.py --job sentiment
python run_local_simulation.py --job daily
python run_local_simulation.py --job sentiment_words
```

---

## 11. REST API Documentation

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

## 12. Testing & Verification

Run backend unit and integration tests:
```powershell
cd backend
python -m pytest -v
```
**Results:** `18 passed in 10.42s (100% pass rate)`.

Verify frontend production build:
```powershell
cd frontend
npm run build
```
**Results:** `✓ built in 11.44s` with 0 errors.

---

## 13. Limitations & Future Enhancements

### Limitations
- Free tier hosting (Render) puts services to sleep after 15 minutes of inactivity; initial wakeup takes ~30-50 seconds.
- Ephemeral container storage on free cloud tiers resets uploaded files on redeployment; bundled sample datasets persist permanently in Git.

### Future Enhancements
- Integration with Apache Kafka and Spark Streaming for live real-time ingestion.
- Multilingual transformer fine-tuning (IndicBERT) for advanced syntactic ambiguity.
- OpenStreetMap geospatial visualization for municipal complaints.

---

## 14. License

This project is licensed under the [MIT License](LICENSE).
