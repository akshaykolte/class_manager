
f = open("pp.txt", "r+")
parent_list = []
for pp in f.readlines():
	parent_list.append('$'.join(pp.split('\t')))
f.close()

f = open("final.txt", "w+")
for p in parent_list:
	f.write(p)
