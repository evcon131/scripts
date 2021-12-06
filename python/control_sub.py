def control_subtractor(infile, control_id):
	import gzip
	import io
	import time
	import sys
	import os
	import glob
	control_file_list=[]
	if '.list' in control_id:
		with open(control_id) as fh:
			for line in fh:
				cfile=line.strip()
				control_file_list.apprnd(cfile)
	else:
		control_file_list=glob.glob(control_id+'*')
	out=''
	cd = {}
	counter=0
	starttime=time.time()
	sys.stdout.write('Starting control read...\n')
	sys.stdout.flush()
	for file in control_file_list:
		with open(file) as fh:
			for line in fh:
				if '#' not in line:
					ll=line.split('\t')
					pos=ll[1]
					ref=ll[3]
					alt=ll[4]
					varient=ref+pos+alt
					if ll[0] not in cd:
						cd[ll[0]]=[varient]
					if ll[0] in cd:
						cd[ll[0]].append(varient)

	sys.stdout.write('Starting control subtraction...\n')
	sys.stdout.flush()

	with open(infile) as fh:
		for line in fh:
			if '#' not in line:
				ll = line.split('\t')
				pos=ll[1]
				ref=ll[3]
				alt=ll[4]
				varient=ref+pos+alt
				if ll[0] not in cd:
					out+=line
				elif ll[0] in cd:
					if varient not in cd[ll[0]]:
						out+=line
	with open('t_filter.csub.vcf', 'w') as fh:
		fh.write(out)
	sys.stdout.write('Shits yeah! Moving on!\n')
	sys.stdout.flush()

if __name__ == '__main__':
	import sys
	control_subtractor(sys.argv[1], sys.argv[2])
