def framshift_finder(infile):
	import gzip
	import io
	import time
	import sys
	import os
	import glob
	import mygene
	glist=[]
	with open(infile) as fh:
		for line in fh:
			if '#' not in line[0]:
				ll=line.split('\t')
				ll=ll[7].split('|')
				if ll[3] not in glist:
					glist.append(ll[3])
				if "frameshift_variant" in ll[1]:
					print(line)
	for item in glist:
		print(item)
if __name__ == '__main__':
	import sys
	framshift_finder(sys.argv[1])


