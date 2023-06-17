from setfit import SetFitModel
import logging

logger = logging.getLogger(__name__)


class SentimentAnalysis:
    model: SetFitModel = SetFitModel.from_pretrained("StatsGary/setfit-ft-sentinent-eval")

    @classmethod
    def predict(cls, text: str):
        pred = cls.model(text)
        return pred

    @classmethod
    def multi_predict(cls, text_array: list[str]):
        preds = cls.model(text_array)
        return preds
