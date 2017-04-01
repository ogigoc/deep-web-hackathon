from search.search import Searcher
from crawler.db_handler import DbHandler

query = "libya"
s = Searcher()
db = DbHandler()

for result in s.get_notevil_results(query):
	db.put_unused_url(result, priority = 40000)

for result in s.get_torch_results(query):
	db.put_unused_url(result, priority = 40000)