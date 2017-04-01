import requests
import json
import queue
import re
import threading
import time
from db_handler import DbHandler

session = requests.session()
session.proxies = {'http' : 'http://10.120.194.45:8123/',
                   'https': 'http://10.120.194.45:8123/'}

my_ip = requests.get("http://httpbin.org/ip").text
tor_ip = session.get("http://httpbin.org/ip").text

if(my_ip == tor_ip):
	print('Not connected to tor. Aborting...')
	quit()

h1 = DbHandler()
visited = h1.get_url_set()
que = queue.Queue()

print('namestio sam')

def parse_link(l, url):
	sol = ""

	#leads to the same page
	if l.find(url) == 0:
		sol = l 
	elif l[0] == '/':
		sol = url + l[1:]
	else:
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
   while not exitFlag:
      #queueLock.acquire()
      if not q.empty():

         url = q.get()

         head = s.head(url)
         if 'Content-Length' in head.headers and int(head.headers['Content-Length']) > 1024 * 100:
         	continue
         r = s.get(url)

         if r:
         	h.put_site(r.url, r.text.replace('\x00', ''))

         reg = re.compile(r'href="([^"]+)')
         good_links = filter_links(reg.findall(r.text), base(r.url))
         
         new_links = [link for link in good_links if link not in visited]

         for link in new_links:
         	if link not in visited:
         		h.put_unused_url(link)
         		visited.add(link)

         #queueLock.release()
         print ("%s processing %s" % (threadID, '1'))
      else:
         #queueLock.release()
         time.sleep(1)

#queueLock = threading.Lock()

threads = []
print('palim tredove')
for id in range(50):
	thread = myThread(id, que, session, DbHandler())
	thread.start()
	threads.append(thread)

print('beskonacna petlja')
#h1.put_unused_url('http://gxamjbnu7uknahng.onion/wiki/index.php/Main_Page')
while 1:
	if que.empty():
		for url in h1.get_unused_batch(1000):
			que.put(url)


"""

# Wait for queue to empty
while not que.empty():
	pass

# Notify threads it's time to exit
exitFlag = 1

# Wait for all threads to complete

for t in threads:
	t.join()
print ("Exiting Main Thread")
"""
