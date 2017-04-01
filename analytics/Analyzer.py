import geograpy
import googlemaps
import json
import requests
import psycopg2
import datetime
from hashlib import sha1

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

class DbHandler:
    def __init__(self):
        connect_str = "dbname='deepweb' user='midza' host='10.120.194.45' password='midza555333!'" 
        self.conn = psycopg2.connect(connect_str) 
        self.cursor = self.conn.cursor() 

    def get_blocks(self, qty):
        self.cursor = self.conn.cursor()
        self.cursor.execute("""SELECT text FROM text_block WHERE LENGTH(text) > 100 LIMIT %s;""", (qty,)) 
        rows = self.cursor.fetchall()
        blocks = [row[0] for row in rows]
        return blocks

    def put_loc_data(self, loc_data):
    	for k, v in loc_data.items():
    		self.cursor.execute("""SELECT name FROM locations WHERE name=%s;""", (k,)) 
        	rows = self.cursor.fetchall()
        	if len(rows) > 0:
        		self.cursor.execute("""UPDATE locations SET qty = qty + %s, pos = pos + %s, neg = neg + %s WHERE name = %s;""",(v[2], v[3], v[4], k))
        	else:
        		self.cursor.execute("""INSERT INTO locations (name, lat, lng, qty, pos, neg) VALUES (%s, %s, %s, %s, %s, %s);""",(k, v[0], v[1], v[2], v[3], v[4]))
    	self.conn.commit()


class GeoAnalyzer:
	def __init__(self):
		self.gmaps = googlemaps.Client(key='AIzaSyB_lS9NW-Ik674_5fzoK10OW0k3xG-Vohc')
		self.loc_data = dict() # name -> (lat, lng, qty, pos, neg)
		self.sent = SentimentAnalyzer()

	def merge_tups(self, tup1, tup2):
		return (tup1[0] + tup2[0], tup1[1] + tup2[1], tup1[2] + tup2[2])

	def do_geocoding(self, location):
		geocode_result = self.gmaps.geocode(location)
		if len(geocode_result) > 0 and 'geometry' in geocode_result[0]:
			geom = geocode_result[0]['geometry']
			if 'location' in geom:
				lat = geom['location']['lat']
				lng = geom['location']['lng']
				return (lat, lng)
		return None

	def fetch_locs(self, text=None, url=None):
		sentiment = self.sent.get_sentiment(text)
		if text:
			text = " ".join(w.capitalize() for w in text.split())
		places = geograpy.get_place_context(text=text, url=url)
		entities = []
		entities.extend(places.countries)
		#entities.extend(places.cities)
		#entities.extend(places.other)
		for name in entities:
			if name in self.loc_data:
				d = self.loc_data[name]
				self.loc_data[name] = (d[0], d[1], d[2] + 1, d[3] + sentiment[0], d[4] + sentiment[1])
			else:
				latlng = self.do_geocoding(name)
				if latlng:
					self.loc_data[name] = latlng + (1,) + sentiment

	def get_loc_data(self):
		return self.loc_data

# url = 'http://www.bbc.com/news/world-europe-26919928'
h = DbHandler()
g = GeoAnalyzer()
s = SentimentAnalyzer()
LEN = 10
blocks = h.get_blocks(LEN)
for i in range(len(blocks)):
	if i % 10 == 0:
		print("BLOCK " + str(i) + " / " + str(len(blocks)))
	g.fetch_locs(text=blocks[i])
print(g.get_loc_data())
h.put_loc_data(g.get_loc_data())

# dodati da li je analizirano u text blocks

# 1. mapa sa polarizovanim pinovima po sigmoidu (globe cak eventualno?!)
# 2. za neku rec what does deep web think?! index