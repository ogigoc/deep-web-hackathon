import requests
import json
import queue
import re
import threading
import time
from .db_handler import DbHandler
from parsing.parser import parse_html
import datetime

session = requests.session()
session.proxies = {'http' : 'http://10.120.194.45:8123/',
        'https': 'http://10.120.194.45:8123/'}

my_ip = requests.get("http://httpbin.org/ip").text
tor_ip = session.get("http://httpbin.org/ip").text

if(my_ip == tor_ip):
    print('Not connected to tor. Aborting...')
    quit()

print('Tor enabled...')

h1 = DbHandler()
visited = h1.get_url_set()
que = queue.Queue()

print('Connected to database...')

def parse_link(l, url):
    sol = ""

    #leads to the same page
    if l.startswith('http://') or l.startswith('https://'):
        sol = l
    elif l.startswith('//'):
        if url.startswith('http://'):
            sol = 'http://' + l[2:]
        elif url.startswith('https://'):
            sol = 'https://' + l[2:]
    elif l[0] == '/':
        sol = base(url) + l[1:]
    else:
        i = l.rfind('/')
        if i == -1:
            sol = ""
        else:
            sol = l[:i + 1] + l

    if len(sol) > 255:
        sol = ""
    """
    if sol != "":
            regex = re.compile(r'\.([^/?=.]+)$')
            ex = regex.search(l)

            if ex and ex.group() not in CONSTANTS.ALLOWED_EXTENSIONS:
                    print(l.encode('utf-8'), file = f_ignored_urls)
                    return ""
    """
    return sol

def filter_links(links, url):
    good_links = []
    for l in links:
            new_url = parse_link(l, url)
            if new_url != "":
                    good_links.append(new_url)
    return good_links

def base(url):
    pos = url.find('.onion')
    if pos == -1:
        return url
    else:
        return url[:pos + 7]


exitFlag = 0
num = 2

def url_priority(url):
    return 50000 if '?' not in url else 100000

class myThread (threading.Thread):
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
        good_links = filter_links(reg.findall(r.text), r.url)

        new_links = [link for link in good_links if link not in visited]

        print('[o] Thread {0} putting results in queue...'.format(threadID))
        i = 0
        for link in new_links:
            if link not in visited:
                #print('stavljam u que'
                i += 1
                h.put_unused_url(link, url_priority(link))
                visited.add(link)
        print('[-] Thread {0} finished putting {1} results in queue.'.format(threadID, i))
        q.task_done()

        #queueLock.release()

#queueLock = threading.Lock()

threads = []
print('[+] Starting threads')
for id in range(3):
    thread = myThread(id, que, session, DbHandler())
    thread.start()
    threads.append(thread)

print('[+] Entering main loop')
while 1:
    que.join()

    i = 0
    for url in h1.get_unused_batch(1000):
        i += 1
        que.put_nowait(url)

    print('[+] Added {0} items to work queue'.format(i))
    if i == 0:
        time.sleep(5)

