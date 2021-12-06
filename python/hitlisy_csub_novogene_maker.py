def hitlist_by_sample(infile, outfile):
	import gzip
	import io
	import time
	import sys
	import os
	import glob
	import mygene
	clist=[]
	out=""
	with open("cfiles.list") as fh:
		for line in fh:
			item=line.strip()
			item=item[0:4]
			clist.append(item)
			print(item)
	with open(infile) as fh:
		for line in fh:
			if not any(item in line for item in clist):
				out+=line

				
	with open(outfile,'w') as fh:
		fh.write(out)

if __name__ == '__main__':
	import sys
	hitlist_by_sample(sys.argv[1], sys.argv[2])
