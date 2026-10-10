import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="SocialPulse 360",
    page_icon="📊",
    layout="wide"
)

st.title("📊 SocialPulse 360")
st.subheader("Social Media Sentiment & Trend Analytics")
st.caption("Tamil-English Social Media Analysis | Powered by Hadoop MapReduce")

st.divider()

# Project paths
BASE_DIR = Path.home() / "SocialPulse360"
DATA_FILE = BASE_DIR / "data" / "processed" / "tamil_sentiment_clean.csv"
SENTIMENT_REPORT = BASE_DIR / "sentiment_report.txt"
TREND_REPORT = BASE_DIR / "trend_report.txt"

# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Choose a page",
    ["Overview", "Sentiment Analysis", "Trend Analytics", "Project Info"]
)

if page == "Overview":
    st.header("Project Overview")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Technology", "Apache Hadoop")
    with col2:
        st.metric("Processing", "MapReduce")

    st.info(
        "This project analyzes Tamil-English social media text "
        "to summarize sentiment categories and frequent words."
    )

elif page == "Sentiment Analysis":
    st.header("Sentiment Analysis")

    if SENTIMENT_REPORT.exists():
        st.text(SENTIMENT_REPORT.read_text(encoding="utf-8"))
    else:
        st.warning("Sentiment report not found.")

elif page == "Trend Analytics":
    st.header("Trend Analytics")

    if TREND_REPORT.exists():
        st.text(TREND_REPORT.read_text(encoding="utf-8"))
    else:
        st.warning("Trend report not found.")

elif page == "Project Info":
    st.header("About SocialPulse 360")

    st.write("**Domain:** Tamil-English Social Media Analytics")
    st.write("**Big Data Technology:** Apache Hadoop MapReduce")
    st.write("**Dashboard Framework:** Streamlit")
    st.write("**Main Features:** Sentiment counts and frequent-word analysis")

    if DATA_FILE.exists():
        st.success("Processed sentiment dataset found.")
    else:
        st.warning("Processed dataset not found at the expected path.")
