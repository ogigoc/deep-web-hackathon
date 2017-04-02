import requests
import json
import queue
import re
import time
import datetime
import crawler.CONSTANTS as CONST
import crawler.db_handler as db_handler
import crawler.net_threads as net_threads

session = requests.session()
session.proxies = {'http' : 'http://10.120.194.45:8123/',
        'https': 'http://10.120.194.45:8123/'}

my_ip = requests.get("http://httpbin.org/ip").text
tor_ip = session.get("http://httpbin.org/ip").text

if(my_ip == tor_ip):
    print('Not connected to tor. Aborting...')
    quit()

print('Tor enabled...')

db = db_handler.DbHandler()
que = queue.Queue()

print('Connected to database...')

threads = []
print('[+] Starting threads')
for id in range(CONST.THREAD_NUMBER):
    thread = net_threads.NetThread(id, que, session, db_handler.DbHandler())
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

