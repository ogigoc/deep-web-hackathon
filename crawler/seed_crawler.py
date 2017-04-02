from crawler.search import Searcher
from crawler.db_handler import DbHandler

s = Searcher()
db = DbHandler()

def seed_crawler(query):
	notevil_results = s.get_notevil_results(query)
	torch_results = s.get_torch_results(query)

	print(len(notevil_results), len(torch_results))

	for result in notevil_results:
		db.put_unused_url(result, priority = 40000)
	for result in torch_results:
		db.put_unused_url(result, priority = 40000)
	return len(notevil_results)+len(torch_results)