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
	if l.find(url) == 0:
		sol = l 
	elif l[0] == '/':
		sol = url + l[1:]
	else:
		sol = ""

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
		#if 'Content-Length' in head.headers and int(head.headers['Content-Length']) > 1024 * 100:
		# 	continue
		tm = time.time()
		r = s.get(url)
		print('retrieved in {0}'.format(1000 * (time.time() - tm)))
		if r.status_code != 200:
			print('[!] Thread {0} received non-zero HTTP status {1} while fetching {2}'.format(threadID, r.status_code, url))

		if r:
			try:
				tm = time.time()
				print('len is {0}'.format(len(r.text)))
				text_blocks = parse_html(r.text)
				print('parsed in {0}'.format(1000 * (time.time() - tm)))

				print('url = {0}'.format(url))
				tittle_list = re.compile(r'<title>([^<]*)<\/title>').findall(r.text)

				tm = time.time()
				h.put_page(url, datetime.datetime.now(), tittle_list[0] if tittle_list else '')
				#print('put page')

				print('put page in {0}'.format(1000 * (time.time() - tm)))
				tm = time.time()

				h.put_text_blocks(url, text_blocks)

				print('put {1} text blocks in {0}'.format(1000 * (time.time() - tm), len([l for lst in text_blocks for l in lst])))

				#print('put text blocks')
			except Exception as e:
				print('faild to parse html or database kurac!')
				print(e)

		reg = re.compile(r'href="([^"]+)')
		good_links = filter_links(reg.findall(r.text), base(r.url))

		new_links = [link for link in good_links if link not in visited]

		print('[o] Thread {0} putting results in queue...'.format(threadID))
		for link in new_links:
			if link not in visited:
				#print('stavljam u que'
				h.put_unused_url(link)
				visited.add(link)
		print('[-] Thread {0} finished putting results in queue.'.format(threadID))

		#queueLock.release()

#queueLock = threading.Lock()

threads = []
print('starting threads...')
for id in range(3):
	thread = myThread(id, que, session, DbHandler())
	thread.start()
	threads.append(thread)

print('entering loop...')
h1.put_unused_url('http://gxamjbnu7uknahng.onion/wiki/index.php/Main_Page')
while 1:
	if que.empty():
		#print('filling the que...')
		for url in h1.get_unused_batch(1000):
			print('[+] Adding {0} to queue'.format(url))
			que.put(url)

