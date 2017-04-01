import requests
import queue
import re
import threading
import CONSTANTS

import concurrent.futures



pages = dict()
que = queue.Queue()

que.put(CONSTANTS.URL)
count = 0
bad_links = set()

log = open('log2.ogi', 'w')
f_bad_links = open('bad_links.txt', 'w')
f_good_links = open('good_links.txt', 'w')
f_ignored_urls = open('ignored_urls.txt', 'w')



def get_request(url, url_number, thread_number):
	
	r = requests.get(url)
	if url_number%50 == 0:
		print(url.encode('utf-8'))
	print(url_number, "thread_number: ", thread_number, " queue_size: ", que.qsize())
	print(url_number, "thread_number: ", thread_number, " queue_size: ", que.qsize(), file = log)
	
	pages[r.url] = ""#chage
	print(r.url.encode('utf-8'), file = f_good_links)
	reg = re.compile(r'<a href="([^"]+)')
	links = filter_links(reg.findall(r.text))
	for l in links:
		if l not in pages:
			pages[l] = ""
			que.put(l)
	return True


def parse_link(l, url):
	sol = ""

	#leads to the same page
	if l.find(url) == 0:
		sol = l 
	elif l[0] == '/':
		sol = url + l[1:]
	else:
		sol = ""

	if sol != "":
		regex = re.compile(r'\.([^/?=.]+)$')
		ex = regex.search(l)

		if ex and ex.group() not in CONSTANTS.ALLOWED_EXTENSIONS:
			print(l.encode('utf-8'), file = f_ignored_urls)
			return ""

	return sol

def filter_links(links):
	good_links = []
	for l in links:
		new_url = parse_link(l, CONSTANTS.URL)
		if new_url != "":
			good_links.append(new_url)
	return good_links

threads = set()
not_alive_for = 0

executor = concurrent.futures.ThreadPoolExecutor(max_workers=CONSTANTS.MAX_THREADS)


while len(threads) != 0 or not que.empty():
	
	#if count > 20:
	#	break
	pom = 0	
	while len(threads) < CONSTANTS.MAX_THREADS and not que.empty():

		count += 1
		t = threading.Thread(target=get_request, args=(que.get(), count, len(threads),))
		threads.add(t)
		t.start()

	#for t in threads:
	#	print(t.is_alive())

		not_alive_for += 1

		rem_tr = []
		for t in threads:
			if not t.is_alive():
				#print("WAITED: ", not_alive_for)
				not_alive_for = 0
				#t.join()
				rem_tr.append(t)
			#threads.remove(t)

		for t in rem_tr:
			threads.remove(t)

	not_alive_for += 1

	rem_tr = []
	for t in threads:
			if not t.is_alive():
				#print("WAITED ------: ", not_alive_for)
				not_alive_for = 0
				#t.join()
				rem_tr.append(t)
			#threads.remove(t)

	for t in rem_tr:
		threads.remove(t)
	
	
#def foo(bar, baz):
#  print 'hello {0}'.format(bar)
#  return 'foo' + baz#
#
#from multiprocessing.pool import ThreadPool
#pool = ThreadPool(processes=1)#

#async_result = pool.apply_async(foo, ('world', 'foo')) # tuple of args for foo

# do some other stuff in the main process

#return_val = async_result.get()  # get the return value from your function.
#