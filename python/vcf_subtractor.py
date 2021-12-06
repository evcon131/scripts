def vcf_subtract(file, file2,outfile):
	import gzip
	import io
	import time
	import sys
	import os
	cd={}
	opt=''
	linecounter=0
	oldtime=time.time()
	starttime=time.time()
	sys.stdout.write('Starting '+str(file2)+' subtraction\n')
	sys.stdout.flush()
	sys.stdout.write('Starting '+str(file2)+' read\n')
	sys.stdout.flush()
	if '.gz' in file2:
		with io.TextIOWrapper(io.BufferedReader(gzip.open(file2))) as fh:
			for line in fh:
				if '#' not in line:
					ll=line.split('\t')
					chroosome=ll[0]
					if 'chr' in chroosome:
						chroosome=chroosome.replace('chr','')
					pos=ll[1]
					ref=ll[3]
					alt=ll[4]
					varient=ref+pos+alt
					if chroosome not in cd:
						cd[chroosome]=[varient]
					elif chroosome in cd:
						cd[chroosome].append(varient)
	elif ".eidx" in file2:
		with open(file2) as fh:
			for line in fh:
				if '#' not in line:
					ll=line.split(',')
					chroosome=ll[0]
					if 'chr' in chroosome:
						chroosome=chroosome.replace('chr','')
					for varient in ll[1:len(ll)]:
						if chroosome not in cd:
							cd[chroosome]=[varient]
						elif chroosome in cd:
							cd[chroosome].append(varient)


	else:
		with open(file2) as fh:
			for line in fh:
				if len(line) > 10:
					if '#' not in line[0]:
						ll=line.split('\t')
						chroosome=ll[0]
						if 'chr' in chroosome:
							chroosome=chroosome.replace('chr','')
						pos=ll[1]
						ref=ll[3]
						alt=ll[4]
						varient=ref+pos+alt
						if chroosome not in cd:
							cd[chroosome]=[varient]
						elif chroosome in cd:
							cd[chroosome].append(varient)
	newtime=time.time()
	timeelapsed = newtime-starttime
	minutes = timeelapsed / 60
	displayminutes=format(minutes, '.2f') 
	oldtime=newtime
	sys.stdout.write(str(file2)+' read done in '+str(displayminutes) +' minutes\nNow starting subtraction\n')
	sys.stdout.flush()
	if '.gz' in file:
		with io.TextIOWrapper(io.BufferedReader(gzip.open(file))) as fh:
			for line in fh:
				if '#' not in line:
					linecounter+=1
					if linecounter % 100000 == 0:
						newtime=time.time()
						timeelapsed = newtime-oldtime
						minutes=timeelapsed / 60
						displayminutes=format(minutes, '.2f') 
						sys.stdout.write(str(linecounter)+' total SNPs processed, last 100k in '+str(displayminutes)+' minutes\n')
						sys.stdout.flush()
						oldtime=newtime
					ll = line.split('\t')
					chroosome=chroosome.replace('chr','')
					pos=ll[1]
					ref=ll[3]
					alt=ll[4]
					varient=ref+pos+alt
					if chroosome not in cd:
						opt+=line
					elif varient not in cd[chroosome]:
						opt+=line
	else:
		with open(file) as fh:
			for line in fh:
				if '#' not in line:
					linecounter+=1
					if linecounter % 100000 == 0:
						newtime=time.time()
						timeelapsed = newtime-oldtime
						minutes=timeelapsed / 60
						displayminutes=format(minutes, '.2f') 
						sys.stdout.write(str(linecounter)+' total SNPs processed, last 100k in '+str(displayminutes)+' minutes\n')
						sys.stdout.flush()
						oldtime=newtime
					ll = line.split('\t')
					chroosome=chroosome.replace('chr','')
					pos=ll[1]
					ref=ll[3]
					alt=ll[4]
					varient=ref+pos+alt
					if chroosome not in cd:
						opt+=line
					elif varient not in cd[chroosome]:
						opt+=line
	with open(outfile,'w') as fh:
		fh.write(opt)
	newtime=time.time()
	timeelapsed = newtime-starttime
	minutes = timeelapsed / 60
	displayminutes=format(minutes, '.2f') 
	sys.stdout.write('total subtraction time '+str(displayminutes)+' minutes\n')
	sys.stdout.flush()

if __name__ == '__main__':
	import sys
	vcf_subtract(sys.argv[1], sys.argv[2], sys.argv[3])
