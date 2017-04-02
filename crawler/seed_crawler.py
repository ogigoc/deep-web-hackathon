from crawler.search import Searcher
from crawler.db_handler import DbHandler

s = Searcher()
db = DbHandler()

def seed_crawler(query):
	
	torch_results = s.get_torch_results(query)

	ahmia_results = s.get_ahmia_results(query)
	for result in ahmia_results[:10]:
		db.put_unused_url(result, priority = 40000)

	candle_results = s.get_candle_results(query)
	for result in candle_results[:10]:
		db.put_unused_url(result, priority = 40000)

	notevil_results = s.get_notevil_results(query)
	for result in notevil_results[:10]:
		db.put_unused_url(result, priority = 40000)

	torch_results = s.get_torch_results(query)
	for result in torch_results[:10]:
		db.put_unused_url(result, priority = 40000)


	#print(len(notevil_results), len(torch_results), len(ahmia_results), len(candle_results))
	print(notevil_results, torch_results, ahmia_results, candle_results)
	return len(notevil_results)+len(torch_results)+len(ahmia_results)+len(candle_results)

seed_crawler('forum')
	