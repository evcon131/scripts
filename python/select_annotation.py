import gzip
import io
import time
import sys
import os
import glob
outputd={}
out=''
with open('t_filter.720sub.csub.vcf') as fh:
	for line in fh:
		if '#' not in line[0]:
			ll=line.split('\t')
			ll=ll[7].split('|')	
			if ('missense_variant' or 'disruptive_inframe_deletion' or 'frameshift_variant' or 'stop_gained' or 'disruptive_inframe_insertion' or 'exon_loss_variant' or 'disruptive_inframe_deletion' or 'start_loss' or 'stop_loss') in ll[1]:
				out+=line

with open('t_filter.720sub.csub.selrctann.vcf','w') as fh:
	fh.write(out)

