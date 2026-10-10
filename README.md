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
