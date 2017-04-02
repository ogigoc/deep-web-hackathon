import psycopg2
import datetime
from hashlib import sha1
import re
from analytics.WordValidator import WordValidator
import crawler.CONSTANTS as CONST

class DbHandler:
    def __init__(self):
        connect_str = "dbname='deepweb' user='midza' host='10.120.193.201' password='midza555333!'" 
        self.conn = psycopg2.connect(connect_str) 
        self.cursor = self.conn.cursor() 

    def put_page(self, url, last_modified, title):
        self.cursor = self.conn.cursor()
        self.cursor.execute("""INSERT INTO newpage (url, timestamp, title) VALUES (%s, now(), %s) ON CONFLICT DO NOTHING;""",(url, title))
        self.conn.commit()

    def put_text_blocks(self, url, text_blocks):
        self.cursor = self.conn.cursor()
        validator = WordValidator()
        for i, lst in enumerate(text_blocks):
            for text_block in lst:
                self.cursor.execute("""INSERT INTO text_block (page_url, text, time, weight, category_id, sha1) VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING;""",
                 (url, text_block.text, text_block.time, text_block.weight, i, sha1(text_block.text.encode('utf-8')).hexdigest()))
                for word in text_block.text.split():
                    if text_block.time:
                        word_clean = re.sub(r"[->!?;.,', ']", "", word).lower().strip()
                        if validator.is_english(word_clean) and not validator.is_stopword(word_clean):
                            self.cursor.execute("""INSERT INTO occurences(word, time) VALUES(%s, %s)""", (word_clean, text_block.time))
        self.conn.commit()

    def get_url_set(self):
        self.cursor = self.conn.cursor()
        self.cursor.execute("""SELECT url from page;""") 
        rows = self.cursor.fetchall()
        urls = set([row[0] for row in rows])
        return urls

    def get_unused_batch(self, sz):
        self.cursor = self.conn.cursor()
        self.cursor.execute("""SELECT id, priority, url FROM unused_urls ORDER BY priority ASC, id ASC LIMIT %s;""",(sz,))
        if self.cursor.rowcount == 0:
            return []
        rows = self.cursor.fetchall()
        urls = [row[2] for row in rows]
        min_id = min([row[0] for row in rows])
        min_priority = min([row[1] for row in rows])
        self.cursor.execute("""DELETE FROM unused_urls WHERE id IN (SELECT id FROM unused_urls ORDER BY priority ASC, id ASC LIMIT %s);""",(sz,)) 
        self.conn.commit()
        return urls
        # list(map(queue.put, urls))

    def put_unused_url(self, url, priority = CONST.PRIORITY_BASE):
        self.cursor = self.conn.cursor()
        self.cursor.execute("""INSERT INTO unused_urls (url, priority) VALUES (%s, %s) ON CONFLICT DO NOTHING;""",(url, priority))
        self.conn.commit()
