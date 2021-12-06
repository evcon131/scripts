import gzip
import io
import time
import sys
import os
import glob
outputd={}
out=''
with open('af_sub_rd_sub.vcf') as fh:
	for line in fh:
		if '#' not in line[0]:
			ll=line.split('\t')
			if ll[0] not in outputd: 
				outputd[ll[0]]=[ll[1]]
				out+line
			if ll[0] in outputd:
				if ll[1] not in outputd[ll[0]]:
					outputd[ll[0]].append(ll[1])
					out+=line

with open('out.vcf','w') as fh:
	fh.write(out)

