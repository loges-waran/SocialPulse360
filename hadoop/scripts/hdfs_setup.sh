#!/bin/bash
# ==============================================================================
# HDFS Setup and Ingestion Script for SocialPulse 360
# ==============================================================================

echo "Initializing HDFS directory structure for SocialPulse 360..."

# Create Directories
hdfs dfs -mkdir -p /socialpulse/input
hdfs dfs -mkdir -p /socialpulse/output
hdfs dfs -mkdir -p /socialpulse/checkpoints

# Upload sample dataset to HDFS
LOCAL_DATA="../../backend/data/sample/sample_social_tanglish_english.csv"
if [ -f "$LOCAL_DATA" ]; then
    echo "Uploading sample dataset to /socialpulse/input/..."
    hdfs dfs -put -f $LOCAL_DATA /socialpulse/input/
    echo "Dataset uploaded. Verifying files on HDFS:"
    hdfs dfs -ls /socialpulse/input/
else
    echo "Sample data not found locally at $LOCAL_DATA"
fi
