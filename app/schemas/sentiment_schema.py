from typing import Literal

from pydantic import BaseModel, validator


class SentimentPOST(BaseModel):
    text: str


class SentimentGET(BaseModel):
    sentiment: Literal['positive', 'negative']
    value: Literal[1, -1]
