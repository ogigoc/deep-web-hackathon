import json
import string
import psycopg2
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from analytics.TrendMode import TrendMode

class TrendsLive:
    def __init__(self):
        connect_str = "dbname='deepweb' user='midza' host='10.120.194.45' password='midza555333!'" 
        self.conn = psycopg2.connect(connect_str) 
        self.cursor = self.conn.cursor() 

    # date_d je datum od kog gledamo pre i posle
    # mode je enum:
    def get_trends(self, date_middle, trend_mode, top):
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
        dur_old = (date_middle - date_old).days + 1
        dur_new = (date_new - date_middle).days + 1
        query = """ SELECT COALESCE(t1.word, t2.word) AS word, 
                           CAST(COALESCE(occ2, 0) AS REAL) / %s * 100 AS wpd2,
                           CAST(COALESCE(occ1, 0) AS REAL) / %s * 100 AS wpd1,
                           CAST(COALESCE(occ2, 0) AS REAL) / %s * 100 - CAST(COALESCE(occ1, 0) AS REAL) / %s * 100 AS wpd_diff
                    FROM (SELECT word, count(time) AS occ1 
                          FROM occurences 
                          WHERE time > %s AND time < %s 
                          GROUP BY word) t1
                    FULL OUTER JOIN
                         (SELECT word, count(time) AS occ2
                          FROM occurences
                          WHERE time > %s AND time < %s
                          GROUP BY word) t2
                       ON t1.word = t2.word
                       ORDER BY wpd_diff DESC
                       LIMIT %s
                """
        self.cursor.execute(query, (dur_new, dur_old, dur_new, dur_old, date_old, date_middle, date_middle, date_new, top))
        rows = self.cursor.fetchall()
        return rows

    def get_occurences(self, word):
        self.cursor.execute("""SELECT time FROM occurences WHERE word = 'brate'""")
        rows = self.cursor.fetchall()
        dates = [row[0] for row in rows]
        return dates

def main():
    t = TrendsLive()
    mid = datetime.strptime('1.3.2016', '%d.%m.%Y')
    rows = t.get_trends(mid, TrendMode.YEAR, 5)
    print(rows)
    for row in rows:
        dates = t.get_occurences(row[0])
        print(row[0] + " (" + str(row[1]) + " - " + str(row[2]) + " " + str(row[3]) + "):")
        print(dates)

if __name__ == "__main__":
    main()
