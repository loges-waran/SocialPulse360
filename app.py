import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="SocialPulse 360",
    page_icon="📊",
    layout="wide"
)

BASE_DIR = Path.home() / "SocialPulse360"
DATA_FILE = BASE_DIR / "data" / "processed" / "tamil_sentiment_clean.csv"
SENTIMENT_REPORT = BASE_DIR / "sentiment_report.txt"
TREND_REPORT = BASE_DIR / "trend_report.txt"

st.title("📊 SocialPulse 360")
st.subheader("Social Media Sentiment & Trend Analytics")
st.caption("Tamil-English Social Media Analysis | Apache Hadoop MapReduce")
st.divider()

if DATA_FILE.exists():
    df = pd.read_csv(DATA_FILE)
    df["sentiment"] = df["sentiment"].astype(str).str.strip()
    df["text"] = df["text"].astype(str).str.strip()

    counts = df["sentiment"].value_counts()
    total = len(df)

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Records", f"{total:,}")
    c2.metric("Sentiment Categories", len(counts))
    c3.metric("Positive Records", f"{counts.get('Positive', 0):,}")

    page = st.sidebar.radio(
        "Navigation",
        ["Overview", "Sentiment Analysis", "Trend Analytics", "Project Info"]
    )

    if page == "Overview":
        st.header("Project Overview")
        st.bar_chart(counts)
        st.info("Dashboard results are calculated from the cleaned dataset.")

    elif page == "Sentiment Analysis":
        st.header("Sentiment Analysis")
        st.subheader("Sentiment Distribution")
        st.bar_chart(counts)
        chart_df = counts.rename_axis("Sentiment").reset_index(name="Records")
        chart_df["Percentage"] = (chart_df["Records"] / total * 100).round(2)
        st.dataframe(chart_df, use_container_width=True, hide_index=True)

        st.subheader("Search Social Media Text")
        query = st.text_input("Enter a word or phrase")
        if query:
            results = df[df["text"].str.contains(query, case=False, na=False)]
            st.write(f"Matching records: {len(results):,}")
            st.dataframe(results.head(100), use_container_width=True, hide_index=True)

    elif page == "Trend Analytics":
        st.header("Trend Analytics")
        st.caption("Most frequent words in the Hadoop MapReduce output")
        if TREND_REPORT.exists():
            st.text(TREND_REPORT.read_text(encoding="utf-8"))
        else:
            st.warning("Trend report not found.")
        st.caption("Word frequency shows common words, not popularity changes over time.")

    else:
        st.header("About SocialPulse 360")
        st.write("**Domain:** Tamil-English Social Media Analytics")
        st.write("**Big Data Technology:** Apache Hadoop")
        st.write("**Processing:** MapReduce")
        st.write("**Dashboard:** Streamlit")
        st.write(f"**Clean dataset records:** {total:,}")
        if SENTIMENT_REPORT.exists():
            st.subheader("Hadoop Sentiment Report")
            st.text(SENTIMENT_REPORT.read_text(encoding="utf-8"))
else:
    st.error(f"Dataset not found: {DATA_FILE}")
    st.info("Check that the cleaned CSV exists at the displayed path.")
