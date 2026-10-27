#!/bin/bash
# ==============================================================================
# SocialPulse 360 - Hadoop Streaming Execution Script (Linux / macOS / WSL)
# ==============================================================================

# Set Hadoop Home and Streaming Jar Path if not preset
HADOOP_HOME=${HADOOP_HOME:-"/usr/local/hadoop"}
STREAMING_JAR=$(find $HADOOP_HOME/share/hadoop/tools/lib/ -name "hadoop-streaming-*.jar" | head -n 1)

if [ -z "$STREAMING_JAR" ]; then
    echo "ERROR: Hadoop Streaming JAR not found in $HADOOP_HOME/share/hadoop/tools/lib/"
    echo "Please ensure Hadoop is properly installed and HADOOP_HOME is configured."
    exit 1
fi

INPUT_DIR=${1:-"/socialpulse/input"}
OUTPUT_BASE=${2:-"/socialpulse/output"}

echo "=========================================================="
echo " Starting SocialPulse 360 Hadoop MapReduce Cluster Jobs   "
echo " Streaming JAR: $STREAMING_JAR"
echo " Input HDFS:    $INPUT_DIR"
echo " Output Base:   $OUTPUT_BASE"
echo "=========================================================="

# Job 1: WordCount
echo "[1/3] Executing WordCount MapReduce Job..."
hdfs dfs -rm -r -f $OUTPUT_BASE/wordcount
hadoop jar $STREAMING_JAR \
    -files ../mapper/wordcount_mapper.py,../reducer/wordcount_reducer.py \
    -mapper "python3 wordcount_mapper.py" \
    -reducer "python3 wordcount_reducer.py" \
    -input $INPUT_DIR \
    -output $OUTPUT_BASE/wordcount

# Job 2: Hashtag Frequency
echo "[2/3] Executing Hashtag Frequency MapReduce Job..."
hdfs dfs -rm -r -f $OUTPUT_BASE/hashtags
hadoop jar $STREAMING_JAR \
    -files ../mapper/hashtag_mapper.py,../reducer/hashtag_reducer.py \
    -mapper "python3 hashtag_mapper.py" \
    -reducer "python3 hashtag_reducer.py" \
    -input $INPUT_DIR \
    -output $OUTPUT_BASE/hashtags

# Job 3: Sentiment Aggregation
echo "[3/3] Executing Sentiment Aggregation MapReduce Job..."
hdfs dfs -rm -r -f $OUTPUT_BASE/sentiment
hadoop jar $STREAMING_JAR \
    -files ../mapper/sentiment_mapper.py,../reducer/sentiment_reducer.py \
    -mapper "python3 sentiment_mapper.py" \
    -reducer "python3 sentiment_reducer.py" \
    -input $INPUT_DIR \
    -output $OUTPUT_BASE/sentiment

echo "=========================================================="
echo " Hadoop MapReduce jobs completed successfully!            "
echo " Use 'hdfs dfs -cat $OUTPUT_BASE/wordcount/part-00000'    "
echo "=========================================================="
