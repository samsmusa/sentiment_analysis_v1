from fastapi import APIRouter, HTTPException, Depends

from app.models.ml_sentiment_analysis import SentimentClassifier
from app.schemas import sentiment_schema
from app.schemas.schemas import HTTPError

api = APIRouter()
model = SentimentClassifier()


@api.post("/sentiment", responses={200: {"model": sentiment_schema.SentimentGET}, 400: {"model": HTTPError}})
def getSentiment(payload: sentiment_schema.SentimentPOST | None = None):
    text = payload.text
    sent = sentiment_schema.SentimentGET(**model.predict(text))
    return sent
