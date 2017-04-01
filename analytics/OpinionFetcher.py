import json
import requests
import psycopg2
import datetime
from scipy.stats import logistic
from functools import reduce
import sys
import getopt

class SentimentAnalyzer:
    def __init__(self):
        self.sess = requests.Session()
        self.SENTIMENT_URL = 'http://text-processing.com/api/sentiment/'

    # http://text-processing.com/docs/sentiment.html
    # returns (positive, negative) tuple adding up to one
    def get_sentiment(self, text):
        r = self.sess.post(self.SENTIMENT_URL, {'text': text})
        res = json.loads(r.text)
        if res['label'] == 'neutral':
            return (0.5, 0.5)
        else:
            return (res['probability']['pos'], res['probability']['neg'])

class OpinionFetcher:
    def __init__(self):
        connect_str = "dbname='deepweb' user='midza' host='10.120.194.45' password='midza555333!'" 
        self.conn = psycopg2.connect(connect_str) 
        self.cursor = self.conn.cursor() 

    def get_verdict(self, summed):
        print(summed)
        if summed[0] == 0 and summed[1] == 0:
            return 'undecided'
        elif summed[0] == 0:
            return 'overwhelmingly negative'
        elif summed[1] == 0:
            return 'overwhelmingly positive'
        else:
            div = summed[0] / summed[1]
            print(div)
            if div < 0.5:
                return 'overwhelmingly negative'
            elif div < 0.95:
                return 'negative'
            elif div < 1.05:
                return 'neutral'
            elif div < 2:
                return 'positive'
            else:
                return 'overwhelmingly positive'

    def fetch(self, sample):
        opinions = []
        self.sen = SentimentAnalyzer()
        self.cursor.execute("""SELECT text from text_block WHERE to_tsvector('english', text)\
                               @@ to_tsquery('english', %s);""", (sample,)) 
        rows = self.cursor.fetchall()
        print("Fetched")
        for row in rows:
            text = row[0]
            sentiment = self.sen.get_sentiment(text)
            opinions.append(sentiment)
        print("Got sents")
        if len(opinions) == 0:
            return "0 mentions of " + sample + "."
        summed = reduce((lambda x, y: (x[0]+y[0], x[1]+y[1])), opinions)
        verdict = self.get_verdict(summed)
        return str(len(opinions)) + " mentions of " + sample + " being " + verdict + " overall."

def main():
    if len(sys.argv) < 2:
        print('Specify the sample')
        exit(0)
    else:
        of = OpinionFetcher()
        result = of.fetch(sys.argv[1])
        print(result)

if __name__ == "__main__":
    main()

# 1. mapa sa polarizovanim pinovima po sigmoidu (globe cak eventualno?!)
# 2. za neku rec what does deep web think?! index