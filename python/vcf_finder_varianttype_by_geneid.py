def vcf_finder_by_geneid(file, qgeneid):
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
				ll=line.split('\t')
				sample_id=ll[len(ll)-1]
				sample_id=sample_id.strip()
				chromosome=ll[0]
				pos=ll[1]
				ref=ll[3]
				alt=ll[4]
				ll=ll[7].split('|')	
				geneid=ll[4]
				if geneid == qgeneid:
					print(ll[1])
if __name__ == '__main__':
	import sys
	vcf_finder_by_geneid(sys.argv[1], sys.argv[2])
