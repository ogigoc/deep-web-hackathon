import requests
import threading
import queue
import time
import datetime
import re
import crawler.db_handler as db_handler
from parsing.parser import parse_html
import crawler.links as links

exitFlag = 0
visited = db_handler.DbHandler().get_url_set()

class NetThread(threading.Thread):
    def __init__(self, threadID, q, s, h):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.q = q
        self.s = s
        self.h = h

    def run(self):
        process_data(self.name, self.q, self.s, self.h)

def process_data(threadID, q, s, h):
    print('[*] Thread {0} starting'.format(threadID))
    while not exitFlag:
        url = q.get()

        print('[o] Thread {0} processing url {1}'.format(threadID, url))

        head = s.head(url)
        if 'Content-Length' in head.headers and int(head.headers['Content-Length']) > 1024 * 100:
            print('[-] Thread {0} encountered content that\'s too long ({0} B)'.format(threadID, head.headers['Content-Length']))
            q.task_done()
            continue

        tm = time.time()
        r = s.get(url)
        #print('retrieved in {0}'.format(1000 * (time.time() - tm)))
        if not r or r.status_code != 200:
            print('[!] Thread {0} received non-zero HTTP status {1} while fetching {2}'.format(threadID, r.status_code, url))
            q.task_done()

        if r:
            try:
                tm = time.time()
                #print('len is {0}'.format(len(r.text)))
                text_blocks = parse_html(r.text)
                #print('parsed in {0}'.format(1000 * (time.time() - tm)))

                #print('url = {0}'.format(url))
                tittle_list = re.compile(r'<title>([^<]*)<\/title>').findall(r.text)

                tm = time.time()
                h.put_page(url, datetime.datetime.now(), tittle_list[0] if tittle_list else '')
                #print('put page')

                #print('put page in {0}'.format(1000 * (time.time() - tm)))
                tm = time.time()

                h.put_text_blocks(url, text_blocks)

                #print('put {1} text blocks in {0}'.format(1000 * (time.time() - tm), len([l for lst in text_blocks for l in lst])))

                #print('put text blocks')
            except Exception as e:
                print('[!] Exception occured when parsing/retrieving! Details: {0}'.format(e))

        reg = re.compile(r'href="([^"]+)')
        good_links = links.filter_links(reg.findall(r.text), r.url)

        new_links = [link for link in good_links if link not in visited]

        print('[o] Thread {0} putting results in queue...'.format(threadID))
        i = 0
        for link in new_links:
            if link not in visited:
                #print('stavljam u que'
                i += 1
                h.put_unused_url(link, links.url_priority(link))
                visited.add(link)
        print('[-] Thread {0} finished putting {1} results in queue.'.format(threadID, i))
        q.task_done()
