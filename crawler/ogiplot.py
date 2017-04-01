from db_handler import DbHandler

h = DbHandler()

s = h.get_url_set()

ns = { x[:15] for x in s }

for u in ns:
	print(u)