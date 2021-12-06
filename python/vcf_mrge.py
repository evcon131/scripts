def filter(tumor_id):
	import gzip
	import io
	import time
	import sys
	import os
	import glob
	sys.stdout.write('Starting File merge\n')
	sys.stdout.flush()
	if '.list' in tumor_id:
		with open(tumor_id) as fh:
			for line in fh:
				tfile=line.strip()
				tumor_file_list.apprnd(tfile)
	else:
		tumor_file_list=glob.glob(tumor_id+'*')	
	out=''
	counter=0
	starttime=time.time()
	for file in tumor_file_list:
		with open(file) as fh:
			counter=0
			for line in fh:
				if '#' not in line[0]:
					line=line.strip()
					sample_id=file[0:-17]
					sample_id=sample_id.strip()
					line+='\t'+sample_id+'\n'
					out+=line
					counter+=1
			sys.stdout.write(file+' had '+str(counter)+'\n')
			sys.stdout.flush()
	with open('t_filter.vcf','w') as fh:
		fh.write(out)
	sys.stdout.write('File merge donezo\n')
	sys.stdout.flush()
if __name__ == '__main__':
	import sys
	filter(sys.argv[1])
