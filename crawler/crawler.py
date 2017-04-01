import requests
import json
import queue
import re
import threading
import time
from db_handler import h

session = requests.session()
session.proxies = {'http':  'http://10.120.194.45:8123/',
                   'https': 'http://10.120.194.45:8123/'}

my_ip = requests.get("http://httpbin.org/ip").text
tor_ip = session.get("http://httpbin.org/ip").text

print(my_ip, tor_ip)

if(my_ip == tor_ip):
	print('Not connected to tor. Aborting...')
	quit()

visited = set()
que = queue.Queue()


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

que.put('http://gxamjbnu7uknahng.onion/wiki/index.php/Main_Page')


exitFlag = 0
num = 2

class myThread (threading.Thread):
   def __init__(self, threadID, q, s):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.q = q
      self.s = s
   def run(self):
      process_data(self.name, self.q, self.s)

def process_data(threadID, q, s):
   while not exitFlag:
      #queueLock.acquire()
      if not q.empty():

         url = q.get()
         r = s.get(url)

         if r and r.url and r.text:
         	h.put_site(r.url, r.text)

         reg = re.compile(r'href="([^"]+)')
         good_links = filter_links(reg.findall(r.text), base(r.url))
         
         new_links = [link for link in good_links if link not in visited]

         for link in new_links:
         	q.put(link)

         #queueLock.release()
         print ("%s processing %s" % (threadID, '1'))
      else:
         #queueLock.release()
         time.sleep(1)

#queueLock = threading.Lock()

threads = []

for id in range(3):
	thread = myThread(id, que, session)
	thread.start()
	threads.append(thread)

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
