import search.search
import crawler.db_handler

dbh = crawler.db_handler.DbHandler()
s = search.search.Searcher()
results = s.get_notevil_results('porn')
for result in results:
	dbh.put_unused_url(result)