import sys
al=[]
file=sys.argv[1]
with open(file) as fh:
	for line in fh:
		if '#' not in line[0]:
			ll=line.split('\t')
			ll=ll[7].split('|')
			if ll[1] not in al:
				al.append(ll[1])
				print(ll[1])
