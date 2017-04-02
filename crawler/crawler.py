import requests
import json
import queue
import re
import time
import datetime
import crawler.CONSTANTS as CONST
import crawler.db_handler as db_handler
import crawler.net_threads as net_threads
import crawler.links as links

session = requests.session()
session.proxies = {'http' : 'http://10.120.194.45:8123/',
        'https': 'http://10.120.194.45:8123/'}

my_ip = requests.get("http://httpbin.org/ip").text
tor_ip = session.get("http://httpbin.org/ip").text

if(my_ip == tor_ip):
    print('Not connected to tor. Aborting...')
    quit()

print('Tor enabled...')

que = queue.Queue()
db = db_handler.DbHandler()
visited = db.get_url_set()
utree = dict()
prios = dict()

visited = set()
for url in CONST.PAGES:
    if url not in visited:
        db.put_unused_url(url, CONST.PRIORITY_SEARCH/2)

for url in visited:
    prios[links.get_url_base(url)] = CONST.BASE_PRIORITY
    for path in links.get_url_path(url):
        if path not in utree:
            utree[path] = 1
        else:
            utree[path] += 1

#print(len(utree))
#print(max(utree.values()))

print('Connected to database...')

threads = []
print('[+] Starting threads')
for id in range(CONST.THREAD_NUMBER):
    thread = net_threads.NetThread(id, que, session, db_handler.DbHandler(), visited, utree, prios)
    thread.start()
    threads.append(thread)

print('[+] Entering main loop')
while 1:
    que.join()

    i = 0
    for url in db.get_unused_batch(CONST.QUEUE_BUFFER_SIZE):
        i += 1
        que.put_nowait(url)

    print('[+] Added {0} items to work queue'.format(i))
    if i == 0:
        time.sleep(3)