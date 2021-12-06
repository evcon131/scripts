def UTR_variant_finder(infile):
	import gzip
	import io
	import time
	import sys
	import os
	import glob
	outputd={}
	out=''
	sys.stdout.write('Starting UTR search\n')
	sys.stdout.flush()
	with open(infile) as fh:
		for line in fh:
			if '#' not in line[0]:
				ll=line.split("\t")
				if "UTR" in ll[7]:
					out+=line
	with open('out.vcf','w') as fh:
		fh.write(out)
if __name__ == '__main__':
	import sys
	UTR_variant_finder(sys.argv[1])