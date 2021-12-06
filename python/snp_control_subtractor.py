import gzip
import io
import time
import sys
import os
import glob
control_file_list=glob.glob('C*')
tumor_file_list=glob.glob('T*')
control_gene_list=[]
tumor_gene_list=[]
out=''
cd = {}
counter=0
starttime=time.time()
for file in control_file_list:
	with open(file) as fh:
		for line in fh:
			if '#' not in line:
				ll=line.split('\t')
				if ll[0] not in cd:
					cd[ll[0]]=[ll[1]]
				if ll[0] in cd:
					cd[ll[0]].append(ll[1])

with open('t_filter.720sub.vcf') as fh:
	for line in fh:
		if '#' not in line:
			ll = line.split('\t')
			if ll[0] not in cd:
				out+=line
			if ll[0] in cd:
				if ll[1] not in cd[ll[0]]:
					out+=line
with open('t_filter.720sub.csub.vcf', 'w') as fh:
	fh.write(out)
