from crawler.search import Searcher
from crawler.db_handler import DbHandler
import crawler.CONSTANTS as CONST

query = "Vietnam"

s = Searcher()
db = DbHandler()

notevil_results = s.get_notevil_results(query)
torch_results = s.get_torch_results(query)

print(len(notevil_results), len(torch_results))

for result in notevil_results:
	db.put_unused_url(result, priority = CONST.PRIORITY_SEARCH)
for result in torch_results:
	db.put_unused_url(result, priority = CONST.PRIORITY_SEARCH)