# SocialPulse 360 — MapReduce Algorithm Specification

This document details the MapReduce jobs implemented in **SocialPulse 360**. Every job adheres strictly to the classic Google MapReduce / Apache Hadoop paradigm:
$$\text{Map}: (k_1, v_1) \rightarrow \text{list}(k_2, v_2)$$
$$\text{Shuffle \& Sort}: \text{list}(k_2, v_2) \rightarrow (k_2, \text{list}(v_2))$$
$$\text{Reduce}: (k_2, \text{list}(v_2)) \rightarrow \text{list}(k_3, v_3)$$

---

## 1. Job 1: Word Count (`WordCount`)

### Objective
Calculate the global frequency of tokens across all cleaned social media posts to identify prevalent terminology.

### Mapper (`hadoop/mapper/wordcount_mapper.py`)
- **Input:** Standard lines of text or CSV records.
- **Processing:**
  1. Filters out handles (`@user`), URLs, and pure timestamp patterns.
  2. Strips punctuation while preserving Tamil Unicode characters ($\text{U}+0\text{B}80$ to $\text{U}+0\text{BFF}$).
  3. Discards English stop words (`the`, `is`, `at`, etc.) and Tanglish conversational particles (`da`, `ah`, `la`, `bro`, `intha`, `nu`).
  4. Emits `(word, 1)` for tokens of length $\ge 3$.
- **Map Output:**
  ```text
  connectivity	1
  infrastructure	1
  innovation	1
  ```

### Reducer (`hadoop/reducer/wordcount_reducer.py`)
- **Input:** Alphabetically sorted `(word, 1)` pairs from the shuffle stage.
- **Processing:** Accumulates counts across contiguous identical keys.
- **Reduce Output:**
  ```text
  connectivity	14
  infrastructure	42
  innovation	28
  ```

---

## 2. Job 2: Hashtag Frequency Counter (`HashtagCount`)

### Objective
Track viral social campaigns, civic initiatives, and community hashtags (`#Tag`).

### Mapper (`hadoop/mapper/hashtag_mapper.py`)
- **Input:** Raw social media text.
- **Processing:** Executes regex `#(\w+)`, normalizes tags to lowercase, and emits `(#hashtag, 1)`.
- **Map Output:**
  ```text
  #chennaimetro	1
  #sdg9	1
  #digitalindia	1
  ```

### Reducer (`hadoop/reducer/hashtag_reducer.py`)
- **Input:** Alphabetically grouped `#hashtag\t1` pairs.
- **Processing:** Sums occurrences for each unique hashtag.
- **Reduce Output:**
  ```text
  #chennaimetro	8
  #digitalindia	12
  #sdg9	15
  ```

---

## 3. Job 3: Sentiment Aggregation (`SentimentAgg`)

### Objective
Aggregate global sentiment counts (`positive`, `negative`, `neutral`) across millions of records.

### Mapper (`hadoop/mapper/sentiment_mapper.py`)
- **Input:** Tab-separated record containing evaluated sentiment label or raw post.
- **Processing:** Extracts sentiment category and emits `(sentiment, 1)`.
- **Map Output:**
  ```text
  positive	1
  negative	1
  positive	1
  ```

### Reducer (`hadoop/reducer/sentiment_reducer.py`)
- **Input:** Sorted `sentiment\t1` pairs.
- **Processing:** Aggregates totals into 3 definitive categories.
- **Reduce Output:**
  ```text
  negative	16
  neutral	11
  positive	22
  ```

---

## 4. Job 4: Daily Sentiment Trends (`DailySentiment`)

### Objective
Compute the sentiment breakdown for each calendar date to evaluate trends over time.

### Mapper (`hadoop/mapper/daily_sentiment_mapper.py`)
- **Input:** Records containing timestamp (`YYYY-MM-DD`) and sentiment label.
- **Processing:** Constructs composite key `date:sentiment` and emits `(date:sentiment, 1)`.
- **Map Output:**
  ```text
  2026-10-21:positive	1
  2026-10-21:negative	1
  2026-10-22:positive	1
  ```

### Reducer (`hadoop/reducer/daily_sentiment_reducer.py`)
- **Input:** Sorted `date:sentiment\t1` pairs.
- **Processing:** Sums counts per date-sentiment combination.
- **Reduce Output:**
  ```text
  2026-10-21:negative	5
  2026-10-21:positive	8
  2026-10-22:neutral	4
  2026-10-22:positive	10
  ```

---

## 5. Job 5: Frequent Words Grouped by Sentiment (`SentimentWords`)

### Objective
Identify the most characteristic words used in positive praise vs. negative grievances.

### Mapper (`hadoop/mapper/sentiment_words_mapper.py`)
- **Input:** Records containing sentiment label and cleaned text.
- **Processing:** For every valid token, emits composite key `sentiment:word\t1`.
- **Map Output:**
  ```text
  positive:semma	1
  positive:fast	1
  negative:mokka	1
  negative:delay	1
  ```

### Reducer (`hadoop/reducer/sentiment_words_reducer.py`)
- **Input:** Sorted `sentiment:word\t1` pairs.
- **Processing:** Sums occurrences of each word within its sentiment category.
- **Reduce Output:**
  ```text
  negative:delay	7
  negative:mokka	9
  negative:waste	12
  positive:mass	11
  positive:semma	14
  positive:super	16
  ```

---

## 6. Execution Modes

SocialPulse 360 supports two execution modes:

1. **Hadoop Streaming Mode (Cluster / Production):**
   Uses `hadoop-streaming.jar` on an Apache Hadoop / HDFS cluster:
   ```bash
   hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
     -files mapper.py,reducer.py \
     -mapper "python3 mapper.py" \
     -reducer "python3 reducer.py" \
     -input /socialpulse/input \
     -output /socialpulse/output/job1
   ```

2. **Local MapReduce Engine (Stand-alone / Demonstration):**
   Implemented in `backend/app/mapreduce/local_runner.py` and `hadoop/scripts/run_local_simulation.py`.
   Pipes input through the exact Mapper process via STDIN, performs an in-memory/external key sort (simulating the shuffle phase), and feeds the grouped key stream into the Reducer process via STDIN. Collects real telemetry (Map In, Map Out, Shuffle Keys, Reduce Out, Duration in ms).
