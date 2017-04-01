import psycopg2 

class DbHandler:
    def __init__(self):
        connect_str = "dbname='deepweb' user='midza' host='10.120.194.45' password='midza555333!'" 
        self.conn = psycopg2.connect(connect_str) 
        self.cursor = self.conn.cursor() 

    def put_site(self, url, html):
        self.cursor.execute("""INSERT INTO sites (url, html) VALUES (%s, %s);""",(url, html))
        self.conn.commit()

    def get_sites(self):
        self.cursor.execute("""SELECT * from sites;""") 
        rows = self.cursor.fetchall() 
        return rows

    def get_url_set(self):
        self.cursor.execute("""SELECT url from sites;""") 
        rows = self.cursor.fetchall()
        urls = set([row[0] for row in rows])
        return urls

    def get_unused_batch(self, sz):
        self.cursor.execute("""SELECT url FROM unused_urls ORDER BY url LIMIT %s;""",(sz,)) 
        rows = self.cursor.fetchall()
        urls = [row[0] for row in rows]
        self.cursor.execute("""DELETE FROM unused_urls WHERE url IN (SELECT url FROM unused_urls ORDER BY url LIMIT %s);""",(sz,)) 
        self.conn.commit()
        return urls
        # list(map(queue.put, urls))

    def put_unused_url(self, url):
        self.cursor.execute("""INSERT INTO unused_urls (url) VALUES (%s);""",(url,))
        self.conn.commit()

    def url_in_sites(self, url):
        self.cursor.execute("""SELECT url FROM sites WHERE url = %s;""",(url,))
        rows = self.cursor.fetchall()
        return len(rows) > 0
        
# h = DbHandler()

