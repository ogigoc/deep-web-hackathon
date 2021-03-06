import requests
from bs4 import BeautifulSoup
import re
from crawler.links import filter_invalid

class Searcher:
	def __init__(self):
		self.session = requests.session()
		self.session.proxies = {'http':  'http://10.120.193.201:8123/',
	                   			'https': 'http://10.120.193.201:8123/'}

		my_ip = requests.get("http://httpbin.org/ip").text
		tor_ip = self.session.get("http://httpbin.org/ip").text
		if(my_ip == tor_ip):
			print('Not connected to tor. Aborting...')
			quit()

	def get_torch_results(self, query):
		reg = re.compile('^\.\/r2d.php\?url=(.*)\&q=.*$')
		url = 'http://xmh57jrzrnw6insl.onion/4a1f6b371c/search.cgi?q={0}&cmd=Search!'.format(query)
		try:
			html = self.session.get(url, timeout = 5).text
			reg = re.compile(r'href="([^"]+)')
			links = reg = reg.findall(html)
			return filter_invalid(links)
		except:
			return []

	def get_notevil_results(self, query):
		reg = re.compile('^\.\/r2d.php\?url=(.*)\&q=.*$')
		url = 'http://hss3uro2hsxfogfq.onion/index.php?q={0}'.format(query)
		try:
			html = self.session.get(url, timeout = 5).text
			soup = BeautifulSoup(html, 'html.parser')
			links = soup.find_all('span', style='color:black;')
			link_texts = [link.text for link in links]
			return filter_invalid(link_texts)
		except:
			return []

		#http://gjobqjj7wyczbqie.onion/?q=canada
	def get_ahmia_results(self, query):
		reg = re.compile('^\.\/r2d.php\?url=(.*)\&q=.*$')
		url = 'http://msydqstlz2kzerdg.onion/search/?q={0}'.format(query)
		try:
			html = self.session.get(url, timeout = 5).text
			reg = re.compile(r'href="([^"]+)')
			links = reg = reg.findall(html)
			return filter_invalid(links)
		except:
			return []

	def get_candle_results(self, query):
		reg = re.compile('^\.\/r2d.php\?url=(.*)\&q=.*$')
		url = 'http://gjobqjj7wyczbqie.onion/?q={0}'.format(query)
		try:
			html = self.session.get(url, timeout = 5).text
			reg = re.compile(r'href="([^"]+)')
			links = reg = reg.findall(html)
			return filter_invalid(links)
		except:
			return []
