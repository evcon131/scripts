import gzip
import io
import time
import sys
import os
from statistics import *
opt=''
linecounter=0
starttime=time.time()
allele_frequewncy_list=[]
read_depth_list= []					
with open('TZL36988.ann.vcf') as fh:
	for line in fh:
		if '#' not in line[0]:
			ll=line.split('\t')
			ll=ll[7].split(';')	
			allele_frequewncy=0
			read_depth=0
			for item in ll[0:-1]:
				if '|' not in item:
					item=item.strip()
					if 'AF' in item[0:2]:
						il=item.split(',')
						item=il[0]
						allele_frequewncy=float(item[3:])
					if 'DP' in item[0:2]:
						read_depth=float(item[3:])
			if (allele_frequewncy > 0.05 and read_depth > 10):
				opt+=line

print(str(mean(allele_frequewncy)))
print(str(mean(read_depth_list)))

