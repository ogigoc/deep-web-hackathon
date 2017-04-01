import psycopg2 

class DbHandler:
    def __init__(self):
        connect_str = "dbname='deepweb' user='midza' host='10.120.194.45' password='midza555333!'" 
        self.conn = psycopg2.connect(connect_str) 
        self.cursor = self.conn.cursor() 

    def put_site(self, url, html):
        self.cursor.execute("""INSERT INTO sites (url, html) VALUES (%s, %s);""",(url, html))
        self.conn.commit()

    def print_sites(self):
        self.cursor.execute("""SELECT * from sites;""") 
        rows = self.cursor.fetchall() 
        print(rows)

    def get_url_set(self):
        self.cursor.execute("""SELECT url from sites;""") 
        rows = self.cursor.fetchall()
        urls = set([row[0] for row in rows])
        print(urls)
        print(type(urls))

h = DbHandler()
h.get_url_set()