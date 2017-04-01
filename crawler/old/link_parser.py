import re
#/[^/]*\.[^/]*$
f = open('good_links.txt', 'r')

regex = re.compile(r'/[^/]+(\.[^/]+)\n')

#print(f.read())

d = dict()

for x in regex.findall(f.read()):
	if x in d.keys():
		d[x] += 1
	else:
		d[x] = 1


for key in d.keys():
	print(key, "  ", d[key])
