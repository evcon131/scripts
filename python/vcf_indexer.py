def vcf_idx(file):
	import gzip
	import io
	import sys
	sys.stdout.write("Startimg run...\n")
	sys.stdout.flush()
	od={}
	opt=''
	if '.gz' in file:
		with io.TextIOWrapper(io.BufferedReader(gzip.open(file))) as fh:
			for line in fh:
				if '#' not in line[0]:
					ll=line.split('\t')
					chroosome=ll[0]
					if 'chr' in chroosome:
						chroosome=chroosome.replace('chr','')
					pos=ll[1]
					ref=ll[3]
					alt=ll[4]
					varient=ref+pos+alt
					if chroosome not in od:
						od[chroosome]=[varient]
					elif chroosome in od:
						od[chroosome].append(varient)

	else:
		for line in fh:
			if '#' not in line[0]:
				ll=line.split('\t')
				chroosome=ll[0]
				if 'chr' in chroosome:
					chroosome=chroosome.replace('chr','')
				pos=ll[1]
				ref=ll[3]
				alt=ll[4]
				varient=ref+pos+alt
				if chroosome not in od:
					od[chroosome]=[varient]
				elif chroosome in od:
					od[chroosome].append(varient)

	for key in od:
		opt+=key+','
		for item in od[key]:
			opt+=item+','
	if '.gz' in file:
		file=file.replace('.gz','')
		file=file+'.eidx'
	else:
		file+='.eidx'
	with open(file, 'w') as fh:
		fh.write(opt)
if __name__ == '__main__':
	import time
	import sys
	import glob
	import os
	import shutil
	starttime=time.time()
	file = sys.argv[1]
	vcf_idx(file)
	newtime=time.time()
	timeelapsed = newtime-starttime
	minutes = timeelapsed / 60
	hours = minutes / 60
	displayminutes=format(minutes, '.2f') 
	displayhours=format(hours, '.2f') 
	if minutes < 60:
		sys.stdout.write('total run time '+str(displayminutes)+' minutes\n')
		sys.stdout.flush()
	else:
		sys.stdout.write('total run time '+str(displayhours)+' hours\n')
		sys.stdout.flush()


