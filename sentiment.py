from transformers import pipeline

sentiment_model = pipeline("sentiment-analysis")

def analyze_sentiment(text):
    r = sentiment_model(text[:512])[0]
    return r["label"], r["score"]
