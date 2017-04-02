import psycopg2
from flask import Flask, request, render_template
import json
from analytics.OpinionFetcher import OpinionFetcher
from analytics.TrendMode import TrendMode
from datetime import datetime, timedelta, timezone
from analytics.TrendsLive import TrendsLive
from crawler.seed_crawler import seed_crawler

app = Flask(__name__, static_folder='./static/dist', template_folder='./static/')

@app.route('/geo', methods=['GET'])
def geo():
    connect_str = "dbname='deepweb' user='midza' host='10.120.194.45' password='midza555333!'" 
    conn = psycopg2.connect(connect_str) 
    cursor = conn.cursor() 
    # give geo stuff
    cursor.execute("""SELECT * FROM locations""") 
    rows = cursor.fetchall()
    rows_obj = [{'lat': row[0], 'lng': row[1], 'num_occ': row[2], 
                 'name': row[3], 'sentiment': row[4] / row[2]} for row in rows]
    return json.dumps(rows_obj)

@app.route('/opinion', methods=['GET'])
def opinion():
    args = request.args
    if 'text' in args.keys():
        text = args.get('text')
        fetcher = OpinionFetcher()
        opinions, verdict = fetcher.fetch(text)
        resp_obj = [{'len': len(opinions), 'verdict': str(verdict), 'opinions': opinions}]
        return json.dumps("")

@app.route('/trends', methods=['GET'])
def trends():
    args = request.args
    if 'date' in args.keys() and 'mode' in args.keys() and 'limit' in args.keys():
        if args.get('mode') == 'W':
            mode = TrendMode.WEEK
        elif args.get('mode') == 'M':
            mode = TrendMode.MONTH
        elif args.get('mode') == 'Y':
            mode = TrendMode.YEAR
        else:
            return json.dumps("Invalid mode")
        date = datetime.utcfromtimestamp(float(args.get('date')))
        limit = args.get('limit')
        tl = TrendsLive()
        trends = tl.get_trends(date, mode, limit)
        trends_dict = [{'word': t[0], 'wpd2': t[1], 'wpd1': t[2], 'wpd_diff': t[3]} for t in trends]
        for trend in trends_dict:
            dates = tl.get_occurences(trend['word'])
            print(dates)
            trend['dates'] = [d.replace(tzinfo=timezone.utc).timestamp() for d in dates]
        return json.dumps(trends_dict)

@app.route('/seed', methods=['POST'])
def seed():
    data = request.get_json()
    if data and data.get('query'):
        results = seed_crawler(data.get('query'))
        return json.dumps("Found " + str(results) + " results.")
    else:
        return json.dumps('Bad request')

if __name__ == '__main__':
    app.run(host='10.120.193.147')
