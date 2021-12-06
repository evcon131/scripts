def tumor_add_ad(tfile, outfile):
	import gzip
	import io
	import time
	import sys
	import os
	import glob
	out=''
	with open(tfile) as fh:
		for line in fh:
			if '#' not in line[0]:
				line=line.strip()
				ll=line.split("\t")
				ann=ll[len(ll)-1]
				annl=ann.split(':')
				ad=annl[1]
				adl=ad.split(',')
				line+='\t'+adl[0]+'\t'+adl[1]
				line+='\n'
				out+=line
	with open(outfile, 'w') as fh:
		fh.write(out)
if __name__ == '__main__':
	import sys
	tumor_add_ad(sys.argv[1], sys.argv[2])

