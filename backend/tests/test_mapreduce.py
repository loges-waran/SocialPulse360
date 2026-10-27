"""
Unit tests for Local MapReduce execution framework.
"""

from app.mapreduce.local_runner import local_mr_runner

def test_wordcount_mapreduce():
    input_text = "hadoop hdfs mapreduce\nhadoop distributed system\nmapreduce hadoop"
    res = local_mr_runner.run_job("WordCount", "wordcount_mapper.py", "wordcount_reducer.py", input_text)
    
    assert res["status"] == "COMPLETED"
    assert res["metrics"]["map_input_records"] == 3
    assert res["metrics"]["reduce_output_records"] > 0
    
    # Check that hadoop was counted 3 times
    parsed = {item["key"]: item["value"] for item in res["parsed_results"]}
    assert parsed.get("hadoop") == 3
    assert parsed.get("mapreduce") == 2
    assert parsed.get("hdfs") == 1

def test_hashtag_mapreduce():
    input_text = "Exciting tech #BigData #Hadoop\nLearning #BigData analytics #SDG9"
    res = local_mr_runner.run_job("HashtagCount", "hashtag_mapper.py", "hashtag_reducer.py", input_text)
    
    assert res["status"] == "COMPLETED"
    parsed = {item["key"]: item["value"] for item in res["parsed_results"]}
    assert parsed.get("#bigdata") == 2
    assert parsed.get("#hadoop") == 1
    assert parsed.get("#sdg9") == 1

def test_sentiment_agg_mapreduce():
    input_text = "id_1\tpositive\nid_2\tpositive\nid_3\tnegative\nid_4\tneutral"
    res = local_mr_runner.run_job("SentimentAgg", "sentiment_mapper.py", "sentiment_reducer.py", input_text)
    
    assert res["status"] == "COMPLETED"
    parsed = {item["key"]: item["value"] for item in res["parsed_results"]}
    assert parsed.get("positive") == 2
    assert parsed.get("negative") == 1
    assert parsed.get("neutral") == 1
