def vcf_printline_by_geneid(file, geneid):
	import gzip
	import io
	import time
	import sys
	import os
	import glob
	import mygene
	mg = mygene.MyGeneInfo()
	slist=[]
	out=''
	refd={}
	with open(file) as fh:
		for line in fh:
			if '#' not in line[0]:
				if geneid in line:
					print(line)
if __name__ == '__main__':
	import sys
	vcf_printline_by_geneid(sys.argv[1], sys.argv[2])

