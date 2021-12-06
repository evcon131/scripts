def bam_sort_script_maker(prefix):
	import glob
	fl=glob.glob(prefix+'*')
	outs='#!/bin/bash\n'
	for file in fl:
		outs+="samtools sort -@ 8 "
		outs+=file+' > '
		outs+=file[0:-3]+'srt.bam\n'
	with open('sort.sh','w') as fh:
		fh.write(outs)
if __name__ == '__main__':
	import sys
	bam_sort_script_maker(sys.argv[1])