import requests
from bs4 import BeautifulSoup
import re

class Searcher:
	def __init__(self):
		self.session = requests.session()
		self.session.proxies = {'http':  'http://10.120.194.45:8123/',
	                   			'https': 'http://10.120.194.45:8123/'}

		my_ip = requests.get("http://httpbin.org/ip").text
		tor_ip = self.session.get("http://httpbin.org/ip").text
		if(my_ip == tor_ip):
			print('Not connected to tor. Aborting...')
			quit()

	def get_notevil_results(self, query):
		reg = re.compile('^\.\/r2d.php\?url=(.*)\&q=.*$')
		url = 'http://hss3uro2hsxfogfq.onion/index.php?q={0}'.format(query)
		html = self.session.get(url).text
		soup = BeautifulSoup(html, 'html.parser')
		links = soup.find_all('span', style='color:black;')
		link_texts = [link.text for link in links]
		return link_texts
