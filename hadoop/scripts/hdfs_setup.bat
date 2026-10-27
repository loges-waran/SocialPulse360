@echo off
REM ==============================================================================
REM HDFS Setup and Ingestion Script for SocialPulse 360 (Windows)
REM ==============================================================================

echo Creating HDFS directory structure for SocialPulse 360...
hdfs dfs -mkdir -p /socialpulse/input
hdfs dfs -mkdir -p /socialpulse/output
hdfs dfs -mkdir -p /socialpulse/checkpoints

set LOCAL_DATA=..\..\backend\data\sample\sample_social_tanglish_english.csv
if exist %LOCAL_DATA% (
    echo Uploading %LOCAL_DATA% to HDFS /socialpulse/input/...
    hdfs dfs -put -f %LOCAL_DATA% /socialpulse/input/
    hdfs dfs -ls /socialpulse/input/
) else (
    echo Sample data file not found.
)
