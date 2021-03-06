import json
import requests
import psycopg2
import datetime
from scipy.stats import logistic
from functools import reduce
import sys
import getopt
from analytics.VaderSentimentAnalyzer import VaderSentimentAnalyzer
from analytics.OpinionClass import OpinionClass

class OpinionFetcher:
    def __init__(self):
        connect_str = "dbname='deepweb' user='midza' host='10.120.193.201' password='midza555333!'" 
        self.conn = psycopg2.connect(connect_str) 
        self.cursor = self.conn.cursor() 
        self.sen = VaderSentimentAnalyzer()

    def fetch(self, sample):
        opinions = []
        self.cursor.execute("""SELECT text from text_block WHERE to_tsvector('english', text)\
                               @@ to_tsquery('english', %s);""", (sample,)) 
        rows = self.cursor.fetchall()
        for row in rows:
            text = row[0]
            sentiment = self.sen.get_sentiment(text)
            opinions.append(sentiment)
        if len(opinions) == 0:
            return ([], self.sen.get_verdict(0))
        avg = sum(opinions) / float(len(opinions))
        verdict = self.sen.get_verdict(avg)
        return (opinions, verdict)

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
# 3. TrendsLive ()
