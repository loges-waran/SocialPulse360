# SocialPulse 360 — College Review Presentation Outline

A slide-by-slide structure tailored for academic project reviews, viva voce, and technical demonstrations.

---

### Slide 1: Title Slide
- **Project Title:** SocialPulse 360 — Social Media Sentiment & Trend Analytics Platform
- **Domain:** Big Data Analytics (BDA), NLP, Distributed Systems
- **Alignment:** UN Sustainable Development Goal 9 (Industry, Innovation & Infrastructure)
- **Team / Presenter:** [Student Name / Roll Number / Department]
- **Supervisor / Guide:** [Guide Name / Faculty Designation]

---

### Slide 2: Project Motivation & Problem Statement
- **Context:** Exponential growth in civic and industrial discourse on social media.
- **The Core Problem:**
  - Standard NLP systems fail to parse regional code-mixed languages like **Tanglish (Tamil-English)**.
  - Relational database management systems (RDBMS) fail to scale for unstructured sentiment and trend aggregation.
  - The gap between academic syllabus theory (Hadoop/MapReduce) and practical software deployment.
- **Our Solution:** A scalable, end-to-end platform powered by Apache Hadoop MapReduce principles and an explainable Tanglish-aware sentiment analyzer.

---

### Slide 3: SDG 9 Alignment (Industry, Innovation & Infrastructure)
- **Target 9.1:** Infrastructure Resilience — Real-time tracking of public transit (Chennai Metro, Southern Railways), road congestion (OMR, NHAI), and public utilities.
- **Target 9.c:** Digital Connectivity — Monitoring telecom outages, fiber expansions, and 5G industrial rollout feedback.
- **Target 9.5:** Technological Capabilities — Indigenous Tanglish NLP engineering without reliance on costly commercial APIs.

---

### Slide 4: System Architecture
- Multi-tier Architecture Diagram:
  - **Data Layer:** File Ingestion, Validation, Schema Detection, HDFS Staging.
  - **Processing Layer:** MapReduce Framework (WordCount, HashtagCount, SentimentAgg, DailySentiment, SentimentWords).
  - **Intelligence Layer:** Hybrid NLP Sentiment Classifier with valence scoring.
  - **Service Layer:** FastAPI REST API with SQLite metadata tracking.
  - **Presentation Layer:** React + Vite responsive dark-themed dashboard.

---

### Slide 5: The Big Data Pipeline & MapReduce Jobs
- Highlight the 5 Core MapReduce Jobs:
  1. **WordCount:** Measures global lexical prevalence.
  2. **HashtagCount:** Identifies trending hashtags (`#Tag`).
  3. **SentimentAgg:** Calculates positive, negative, and neutral proportions.
  4. **DailySentiment:** Tracks temporal sentiment changes over calendar dates.
  5. **SentimentWords:** Categorizes frequent words by sentiment emotion.
- Emphasize the **Shuffle and Sort phase** and explain why MapReduce is mathematically superior to simple single-threaded groupby for big data.

---

### Slide 6: Tanglish NLP & Explainable Sentiment Engine
- How Tanglish is processed:
  - **Tokenization & Stop Words:** Filtering out conversational particles (`da`, `ah`, `la`, `bro`, `intha`).
  - **Transliterated Lexicon:** Valence scores for Romanized Tamil terms (*semma* = +3.4, *mokka* = -3.2, *vera level* = +3.8).
  - **Context Modifiers:** Intensifiers (*romba*, *semmaya*) and Negations (*illa*, *mudiyala*).
  - **Normalized Compound Score:** Range from $-1.0$ to $+1.0$ with confidence calibration.

---

### Slide 7: Live Demonstration & UI Showcase
- **Overview Dashboard:** Total records, KPIs, sentiment donut chart, processing duration.
- **Sentiment Analytics:** Donut & bar charts, daily timeline trend curves, key emotional drivers.
- **Trend Analytics:** Top 10/20/50 words, trending hashtags, positive vs. negative keyword comparison.
- **Dataset Explorer:** Filterable records table with original vs. cleaned text and sentiment tags.
- **MapReduce Telemetry Monitor:** Live inspection of input records, emitted pairs, distinct keys, reducer outputs, and actual Python Mapper/Reducer source code.

---

### Slide 8: Experimental Results & Performance Metrics
- Total records verified: 48 sample records.
- MapReduce emitted pairs: 833 (WordCount), 270 (Hashtags).
- Sub-second pipeline execution (280 ms local simulation).
- 18 / 18 Automated unit and integration tests passing.

---

### Slide 9: Conclusion & Future Scope
- **Conclusion:** Successfully achieved an industry-standard, fully functional Big Data mini-project demonstrating Hadoop MapReduce, NLP, and modern UI engineering.
- **Future Scope:**
  - Real-time streaming integration with Apache Kafka and Apache Spark Streaming.
  - Fine-tuning a multilingual RoBERTa / IndicBERT model for complex syntactic nuances.
  - Automated geospatial tweet clustering for municipal alert notifications.

---

### Slide 10: Questions & Discussion (Q&A)
- Open the floor for review panel questions.
