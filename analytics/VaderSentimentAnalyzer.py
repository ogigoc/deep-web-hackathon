from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from analytics.OpinionClass import OpinionClass

class VaderSentimentAnalyzer:
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()

    def get_sentiment(self, text):
        vs = self.analyzer.polarity_scores(text)
        return vs['compound']

    def get_verdict(self, div):
        if div < -0.5:
            return OpinionClass.VERY_NEGATIVE
        elif div < -0.1:
            return OpinionClass.NEGATIVE
        elif div < 0.1:
            return OpinionClass.NEUTRAL
        elif div < 0.5:
            return OpinionClass.POSITIVE
        else:
            return OpinionClass.VERY_POSITIVE
