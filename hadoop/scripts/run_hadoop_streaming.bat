@echo off
REM ==============================================================================
REM SocialPulse 360 - Hadoop Streaming Execution Script for Windows
REM ==============================================================================

if "%HADOOP_HOME%"=="" (
    echo ERROR: HADOOP_HOME environment variable is not defined.
    echo Please set HADOOP_HOME or run local simulation via run_local_simulation.py
    pause
    exit /b 1
)

set STREAMING_JAR=%HADOOP_HOME%\share\hadoop\tools\lib\hadoop-streaming-3.3.6.jar
set INPUT_HDFS=/socialpulse/input
set OUTPUT_HDFS=/socialpulse/output

echo ==========================================================
echo  Starting SocialPulse 360 Hadoop MapReduce Windows Job
echo  Input HDFS:  %INPUT_HDFS%
echo  Output HDFS: %OUTPUT_HDFS%
echo ==========================================================

REM Job 1: Word Count
hdfs dfs -rm -r -f %OUTPUT_HDFS%/wordcount
call hadoop jar %STREAMING_JAR% ^
    -files ..\mapper\wordcount_mapper.py,..\reducer\wordcount_reducer.py ^
    -mapper "python wordcount_mapper.py" ^
    -reducer "python wordcount_reducer.py" ^
    -input %INPUT_HDFS% ^
    -output %OUTPUT_HDFS%/wordcount

REM Job 2: Hashtag Frequency
hdfs dfs -rm -r -f %OUTPUT_HDFS%/hashtags
call hadoop jar %STREAMING_JAR% ^
    -files ..\mapper\hashtag_mapper.py,..\reducer\hashtag_reducer.py ^
    -mapper "python hashtag_mapper.py" ^
    -reducer "python hashtag_reducer.py" ^
    -input %INPUT_HDFS% ^
    -output %OUTPUT_HDFS%/hashtags

echo Jobs completed!
