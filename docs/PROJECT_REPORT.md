# SocialPulse 360: Social Media Sentiment & Trend Analytics Platform
## Academic Mini Project Report — Big Data Analytics (BDA)

---

### Abstract

The massive growth of decentralized social media platforms has transformed public discourse into an abundant stream of real-time civic, cultural, and industrial feedback. However, extracting actionable intelligence from regional social media streams presents substantial big data challenges: high volume, unstructured text, noise, and complex linguistic code-mixing—specifically **Tamil-English (Tanglish)** and **Tamil Unicode** alongside English. Conventional centralized relational databases and naive keyword algorithms fail to scale effectively over large corpora or misclassify regional sentiment.

**SocialPulse 360** is an industry-standard, end-to-end Big Data Analytics project designed to solve these challenges. The platform implements distributed processing concepts using **Apache Hadoop, HDFS, and MapReduce** alongside an explainable, multi-stage Natural Language Processing (NLP) pipeline. The architecture supports two execution modes: cluster execution via **Hadoop Streaming** and a standalone **Local MapReduce Engine** that faithfully replicates the Mapper $\rightarrow$ Sort/Shuffle $\rightarrow$ Reducer lifecycle with real telemetry. The platform analyzes positive, negative, and neutral sentiments, tracks viral hashtags and trending words, isolates sentiment-specific expressions, and visualizes daily sentiment trajectories over time. The project is aligned with **United Nations Sustainable Development Goal 9 (Industry, Innovation, and Infrastructure)** to monitor public sentiment on mass transit, energy grids, and digital communication networks.

---

### 1. Problem Statement & Objectives

#### 1.1 Problem Statement
Urban citizens and industrial stakeholders frequently broadcast urgent feedback regarding public transport breakdowns, telecom outages, and infrastructure projects on social media. Much of this regional discourse in Southern India is expressed in **Tanglish** (Romanized phonetic Tamil mixed with English). Existing analytics tools are either:
1. Monolingual English tools that treat Tanglish words (e.g., *semma, mokka, waste, vera level*) as out-of-vocabulary noise.
2. Proprietary cloud APIs that are opaque, expensive, and do not demonstrate distributed Big Data processing paradigms required by the university curriculum.
3. Centralized scripts that choke on large social datasets.

#### 1.2 Project Objectives
1. **Demonstrate Core Big Data Principles:** Implement real MapReduce jobs for Word Count, Hashtag Counting, Sentiment Aggregation, Daily Timeline Tracking, and Sentiment-Word Grouping.
2. **Develop a Robust NLP Sentiment Engine:** Accurately classify English, Tamil script, and Tanglish text with explainable valence ratings, booster multipliers, and negation detection.
3. **Build an Interactive Web Dashboard:** Provide a responsive dark-themed analytics portal in React and Vite with Recharts, enabling dataset uploads, live telemetry inspection, and CSV data export.
4. **Advance SDG 9:** Provide quantifiable sentiment indicators regarding infrastructure reliability, digital connectivity, and industrial innovation.

---

### 2. Existing System vs. Proposed System

| Dimension | Existing Systems | Proposed System (SocialPulse 360) |
| :--- | :--- | :--- |
| **Processing Paradigm** | Monolithic in-memory Pandas `groupby` operations; crashes on memory overflow. | Scalable **Hadoop MapReduce** architecture with streaming mappers, key partitioning, and reducers. |
| **Language Support** | Standard English only; fails on Romanized Tamil (Tanglish). | **Bilingual & Code-Mixed NLP**: English, Tanglish, and Tamil Unicode lexicon with negation/booster awareness. |
| **Hadoop Integration** | Often only present in theoretical documentation. | **Actual Mapper & Reducer scripts** with verified execution, HDFS scripts, and a Local MapReduce simulation engine. |
| **Explainability** | Opaque black-box sentiment classification without breakdown. | Fully explainable: matched tokens, valence weights, compound normalization, and confidence scores. |
| **UI/UX Design** | Static Jupyter notebooks or rudimentary command-line output. | Modern, glassmorphism **React + Tailwind** dashboard with Recharts, live code inspection, and CSV export. |

---

### 3. System Architecture & Methodology

```
+-------------------------------------------------------------------------+
|                        Data Sources & Ingestion                         |
|      (Sample Datasets, User CSV Uploads, JSON Social Media Feeds)       |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
|                  Data Validation & Cleaning Pipeline                     |
|  - Auto-detect schema (text, timestamp, hashtags, author)               |
|  - Deduplication & missing value imputation                             |
|  - Emoji normalization, URL stripping, user handle extraction           |
|  - Preserves original_text; generates cleaned_text                      |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
|                    Hybrid NLP Sentiment Classifier                      |
|  - Language Tagging (English, Tanglish, Tamil)                          |
|  - Transliterated Tanglish Lexicon (semma, mokka, vera level)           |
|  - Valence scoring with boosters (romba, very) & negators (illa, not)   |
|  - Normalized Compound Score [-1.0, +1.0] and Calibrated Confidence     |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
|               Hadoop HDFS / Local Staging Data Layer                    |
|           /socialpulse/input/ (Formatted streaming TSV files)           |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
|               Hadoop MapReduce Processing (5 Core Jobs)                 |
|  1. WordCount:        word_mapper.py        -> word_reducer.py          |
|  2. HashtagCount:     hashtag_mapper.py     -> hashtag_reducer.py       |
|  3. SentimentAgg:     sentiment_mapper.py   -> sentiment_reducer.py     |
|  4. DailySentiment:   daily_mapper.py       -> daily_reducer.py         |
|  5. SentimentWords:   sent_words_mapper.py  -> sent_words_reducer.py    |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
|                  Trend Aggregation & SQLite Catalog                     |
|  - Top 10/20/50 words, viral hashtags, daily timeline trajectories      |
|  - Persistence of job execution telemetry, runtimes, and output metrics |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
|              FastAPI REST Backend (Swagger Docs /docs)                  |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
|                 Modern React + Vite Analytics Dashboard                 |
|     (Overview, Sentiment Donut, Trends, Dataset Explorer, MR Monitor)   |
+-------------------------------------------------------------------------+
```

---

### 4. MapReduce Mathematical Formulation

The MapReduce engine partitions the analytical workload across mapper and reducer tasks:

1. **Map Step:**
   Given a streaming line $L$, the Mapper extracts token $w$ and emits:
   $$\text{Emit}(w, 1)$$

2. **Shuffle and Sort Step:**
   All emitted pairs are partitioned and sorted by key:
   $$K = \{w_1, w_2, \dots, w_k\}, \quad V(w_i) = [1, 1, \dots, 1]$$

3. **Reduce Step:**
   The Reducer aggregates the grouped values:
   $$\text{Count}(w_i) = \sum_{v \in V(w_i)} v$$
   $$\text{Emit}(w_i, \text{Count}(w_i))$$

---

### 5. Experimental Results

The platform was verified using real sample datasets containing English, Tanglish, and Tamil social media posts:

- **Total Records Processed:** 48 sample records & 15,601 full benchmark Tamil records
- **Map Input Records:** 48 lines (sample) / 15,601 lines (benchmark)
- **Total Map Output Pairs Emitted:** 833 pairs (WordCount), 270 pairs (HashtagCount)
- **Distinct Partitioned Keys:** 529 keys (WordCount), 106 keys (HashtagCount)
- **Sentiment Distribution (Sample):**
  - Positive: 45.83% (22 posts)
  - Negative: 33.33% (16 posts)
  - Neutral: 20.83% (10 posts)
- **Pipeline Execution Latency:** ~280 ms (sample) / ~8.8s (15,601 records)
- **Automated Tests:** 18 out of 18 unit and integration tests passed with 100% success rate.
- **Production Live Deployment:**
  - **Live Web Dashboard:** [https://social-pulse360.vercel.app/](https://social-pulse360.vercel.app/) (Vercel)
  - **Live Backend API & Swagger Docs:** [https://socialpulse360.onrender.com/docs](https://socialpulse360.onrender.com/docs) (Render)
  - **Health Check Endpoint:** [https://socialpulse360.onrender.com/api/health](https://socialpulse360.onrender.com/api/health)

---

### 6. Frequently Asked Questions (Viva / Review Guide)

**Q1: How does Hadoop Streaming differ from native Java MapReduce?**  
*Answer:* Native MapReduce requires writing Java classes using Hadoop's `Mapper` and `Reducer` interfaces. Hadoop Streaming is an official Hadoop utility that enables writing Mappers and Reducers in any executable language (Python, C++, Bash). Hadoop communicates with the scripts via standard input (`stdin`) and standard output (`stdout`), passing tab-separated key-value pairs.

**Q2: What is the purpose of the Shuffle and Sort phase in MapReduce?**  
*Answer:* The Shuffle phase transfers mapper output across the network to the appropriate reducers based on a partitioning hash function. The Sort phase sorts all key-value pairs alphabetically by key, ensuring that each reducer receives all values for a particular key contiguously.

**Q3: How does SocialPulse 360 handle systems where Hadoop is not installed?**  
*Answer:* The application implements a standalone `LocalMapReduceRunner` in Python that replicates the exact MapReduce lifecycle: streaming input to the Mapper script process via STDIN, alphabetically sorting the emitted key-value pairs, and streaming the sorted stream to the Reducer script process. This guarantees that the outputs are 100% verifiable and identical to Hadoop cluster results.

**Q4: How does the system handle code-mixed Tanglish?**  
*Answer:* Tanglish words use English letters to write Tamil phonetics (e.g., *semma, mokka, vera level*). The sentiment engine incorporates a curated Tanglish valence lexicon, detects code-mixed language markers, applies booster modifiers (e.g., *romba, semmaya*), and checks for trailing negations (e.g., *nalla illa* $\rightarrow$ inverted valence).
