import gzip
import io
import time
import sys
import os
from statistics import *
opt=''
linecounter=0
starttime=time.time()
with open('t_filter.720sub.csub.selrctann.vcf') as fh:
	for line in fh:
		if '#' not in line[0]:
			ll=line.split('\t')
			ll=ll[9].split(':')	
			AD=ll[1]
			ll2=AD.split(',')
			read_depth=float(ll2[1])
			if float(ll2[0]) == 0:
				allele_frequewncy=1
			else:
				allele_frequewncy=float(ll2[1])/float(ll2[0])
			if (allele_frequewncy > .05) and (read_depth > 10):
				opt += line
with open('t_filter.720sub.csub.selectann.af_rd.vcf', 'w') as fh:
	fh.write(opt)

