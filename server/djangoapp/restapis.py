import os
import requests
from dotenv import load_dotenv

load_dotenv()

backend_url = os.getenv('backend_url', default="http://localhost:3030")
sentiment_analyzer_url = os.getenv('sentiment_analyzer_url', default="http://localhost:5050/")


def get_request(endpoint, **kwargs):
    params = ""
    if kwargs:
        for key, value in kwargs.items():
            params = params + key + "=" + str(value) + "&"
    request_url = backend_url + endpoint
    if params:
        request_url += "?" + params.rstrip("&")

    try:
        response = requests.get(request_url, timeout=3)
        return response.json()
    except Exception as err:
        # Microservice unreachable
        return None


def analyze_review_sentiments(text):
    request_url = sentiment_analyzer_url.rstrip("/") + "/analyze/" + text
    try:
        response = requests.get(request_url, timeout=3)
        return response.json()
    except Exception:
        # Local fallback using NLTK SentimentIntensityAnalyzer
        try:
            from nltk.sentiment import SentimentIntensityAnalyzer
            sia = SentimentIntensityAnalyzer()
            scores = sia.polarity_scores(text)
            pos = float(scores['pos'])
            neg = float(scores['neg'])
            neu = float(scores['neu'])
            res = "positive"
            if neg > pos and neg > neu:
                res = "negative"
            elif neu > neg and neu > pos:
                res = "neutral"
            return {"sentiment": res}
        except Exception:
            return {"sentiment": "neutral"}


def post_review(data_dict):
    request_url = backend_url.rstrip("/") + "/insert_review"
    try:
        response = requests.post(request_url, json=data_dict, timeout=3)
        return response.json()
    except Exception:
        return None
