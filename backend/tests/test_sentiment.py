"""
Unit tests for English and Tanglish Sentiment Analysis Engine.
"""

from app.sentiment.engine import sentiment_engine

def test_english_positive():
    res = sentiment_engine.analyze("High-speed optical fiber connectivity is expanding! Truly great milestone.")
    assert res["sentiment"] == "positive"
    assert res["score"] > 0.05
    assert res["confidence"] >= 0.60

def test_english_negative():
    res = sentiment_engine.analyze("The latest software patch broke our automated pipeline. Complete disaster and waste.")
    assert res["sentiment"] == "negative"
    assert res["score"] < -0.05
    assert res["confidence"] >= 0.60

def test_tanglish_positive():
    res = sentiment_engine.analyze("Intha movie semma mass ah irukku! Background music vera level!")
    assert res["sentiment"] == "positive"
    assert res["language"] == "tanglish"
    assert res["score"] > 0.10

def test_tanglish_negative():
    res = sentiment_engine.analyze("Worst customer service, 3 days ah internet cut, romba mokka response and waste!")
    assert res["sentiment"] == "negative"
    assert res["language"] == "tanglish"
    assert res["score"] < -0.10

def test_neutral_announcement():
    res = sentiment_engine.analyze("Anna University published examination schedule for autonomous engineering colleges.")
    assert res["sentiment"] == "neutral"
    assert abs(res["score"]) < 0.10

def test_negation_inversion():
    res_pos = sentiment_engine.analyze("The acting was good.")
    res_neg = sentiment_engine.analyze("The acting was not good.")
    assert res_pos["score"] > res_neg["score"]
