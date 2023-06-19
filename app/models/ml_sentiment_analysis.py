import logging
import re
from time import time

import emoji
from setfit import SetFitModel

logger = logging.getLogger('uvicorn')


class SingletonClass(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SingletonClass, cls).__new__(cls)
        return cls.instance


def clean_text(text):
    replacements = [
        (r'[\.]+', '.'),
        (r'[\!]+', '!'),
        (r'[\?]+', '!'),
        (r'\s+', ' '),
        (r'@\w+', ''),
        (r'\s[n]+[o]+', ' no'),
        (r'n\'t', 'n not'),
        (r'\'nt', 'n not'),
        (r'\'re', ' are'),
        (r'\'s', ' is'),
        (r'\'d', ' would'),
        (r'\'ll', ' will'),
        (r'\'ve', ' have'),
        (r'\'m', ' am'),
        (r'\s[n]+[o]+[p]+[e]+', ' no'),
        (r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%|\~)*\b', ''),
        (r'(www.)(\w|\.|\/|\?|\=|\&|\%)*\b', ''),
        (r'\w+.com', '')
    ]

    for pattern, replacement in replacements:
        text = re.sub(pattern, replacement, text, flags=re.MULTILINE).strip()
        logger.info(text)

    text = emoji.demojize(text)
    return text


class SentimentClassifier:
    logger.info('Loading SetFit sentiment classifier ...')
    start = time()
    model: SetFitModel = SetFitModel.from_pretrained("StatsGary/setfit-ft-sentinent-eval")
    logger.info(f'Time taken to load SetFit sentiment classifier = {time() - start}')

    def predict(self, text):
        text = clean_text(text)
        logger.info(f'cleaned text : {text}')
        start = time()
        output = self.model([text])
        logger.info(f'Inference time = {time() - start}')
        return {"sentiment": 'positive', "value": 1} if output.item() == 1 else {"sentiment": 'negative', "value": -1}
