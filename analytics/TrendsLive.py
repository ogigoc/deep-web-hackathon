import json
import string
import psycopg2
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

class TrendsLive:
	def __init__(self):
        connect_str = "dbname='deepweb' user='midza' host='10.120.194.45' password='midza555333!'" 
        self.conn = psycopg2.connect(connect_str) 
        self.cursor = self.conn.cursor() 

    # date_d je datum od kog gledamo pre i posle
    # mode je enum:
    def get_trends(self, date_middle, trend_mode):
    	# durationi oba
    	if trend_mode == TrendMode.WEEK:
    		delta = relativedelta(weeks = 1)
    	elif trend_mode == TrendMode.MONTH:
    		delta = relativedelta(months = 1)
    	elif trend_mode == TrendMode.YEAR:
    		delta = relativedelta(years = 1)
    	else:
    		raise("This should never happen")
    	date_old = date_middle - delta
    	date_new = min(datetime.now(), date_middle + delta)
    	dur_old = (date_middle - date_old).days
    	dur_new = (date_new - date_middle).days
    	query = """SELECT COALESCE(tab1.word, tab2.word) AS word, COALESCE(t2, 0) / dur_new - COALESCE(t1, 0) / 365.0 as wpd_diff FROM
(SELECT word, count(time) as t1 FROM occurences WHERE time > DATE '2015-01-01' AND time <  DATE '2016-01-01' GROUP BY word) tab1
FULL OUTER JOIN
(SELECT word, count(time) as t2 FROM occurences WHERE time > DATE '2017-01-01'  AND time < DATE '2018-01-01'  GROUP BY word) tab2
ON tab1.word = tab2.word
ORDER BY wpd_diff DESC
LIMIT 10

    	"""

        self.cursor.execute(query, (dur_new, dur_old, date_old, date_middle, date_middle, date_new))
        rows = self.cursor.fetchall()


        rows = self.cursor.fetchall()
        for row in rows:
            text = row[0]
            sentiment = self.sen.get_sentiment(text)
            opinions.append(sentiment)
        if len(opinions) == 0:
            return "0 mentions of " + sample + "."
        avg = sum(opinions) / float(len(opinions))
        verdict = self.sen.get_verdict(avg)
        return str(len(opinions)) + " mentions of " + sample + " being " + verdict + " overall."

def main():

# plotovanje lokacija koje se pojavljuju + sentiment
# neka rec + sentiment u vezi nje

s = SentimentAnalyzer()
print(s.get_sentiment('I love trains'))