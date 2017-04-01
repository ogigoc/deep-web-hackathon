from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class VaderSentimentAnalyzer:
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()

    def get_sentiment(self, text):
        vs = self.analyzer.polarity_scores(text)
        return vs['compound']

    def get_verdict(self, div):
        print(div)
        if div < -0.5:
            return 'overwhelmingly negative'
        elif div < -0.1:
            return 'negative'
        elif div < 0.1:
            return 'neutral'
        elif div < 0.5:
            return 'positive'
        else:
            return 'overwhelmingly positive'
