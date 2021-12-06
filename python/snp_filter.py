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
counter=0
starttime=time.time()
for file in tumor_file_list:
	with open(file) as fh:
		counter=0
		for line in fh:
			if '#' not in line[0]:
				ll=line.split('\t')
				ll=ll[7].split('|')
				if ll[5] != 'intergenic_region':
					if ll[7] == 'protein_coding':
						if ll[1] != 'synonymous_variant':
							line=line.strip()
							line+='\t'+file[0:-8]+'\n'
							out+=line
							counter+=1
		sys.stdout.write(file+' had '+str(counter)+'\n')
		sys.stdout.flush()
with open('t_filter.vcf','w') as fh:
	fh.write(out)
