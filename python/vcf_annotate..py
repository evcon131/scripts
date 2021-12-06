def vcf_ann(infile, anfile, outfile='out.vcf'):
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
	oldtime=starttime
	sys.stdout.write('Starting '+str(infile)+' annotate\n')
	sys.stdout.flush()
	sys.stdout.write('Starting '+str(anfile)+' read\n')
	sys.stdout.flush()
	if '.gz' in anfile[len(anfile)-3:]:
		with io.TextIOWrapper(io.BufferedReader(gzip.open(anfile))) as fh:
			for line in fh:
				if '#' not in line[0]:
					linecounter+=1
					if linecounter % 1000000 == 0:
						newtime=time.time()
						timeelapsed = newtime-oldtime
						minutes=timeelapsed / 60
						displayminutes=format(minutes, '.2f') 
						sys.stdout.write(str(linecounter)+' total variants processed, last 1M in '+str(displayminutes)+' minutes\n')
						sys.stdout.flush()
						oldtime=newtime
					ll=line.split('\t')
					chroosome=ll[0]
					if 'chr' in chroosome:
						chroosome=chroosome.replace('chr','')
					pos=ll[1]
					ref=ll[3]
					alt=ll[4]
					variant=ref+pos+alt
					if chroosome not in cd:
						cd[chroosome]=[variant]
					elif chroosome in cd:
						cd[chroosome].append(variant)
	elif ".eidx" in anfile[len(anfile)-5:]:
		with open(anfile) as fh:
			for line in fh:
				if '#' not in line[0]:
					ll=line.split(",")
					chroosome=ll[0]
					if 'chr' in chroosome:
						chroosome=chroosome.replace('chr','')
					for variant in ll[1:len(ll)+1]:
						linecounter+=1
						if linecounter % 10000000 == 0:
							newtime=time.time()
							timeelapsed = newtime-oldtime
							displayseconds=format(timeelapsed, '.2f') 
							sys.stdout.write(str(linecounter)+' total variants processed, last 10M in '+str(displayseconds)+' seconds\n')
							sys.stdout.flush()
							oldtime=newtime
							if chroosome not in cd:
								cd[chroosome]=[variant]
							elif chroosome in cd:
								cd[chroosome].append(variant)
	else:
		with open(anfile) as fh:
			for line in fh:
				if '#' not in line[0]:
					linecounter+=1
					if linecounter % 1000000 == 0:
						newtime=time.time()
						timeelapsed = newtime-oldtime
						minutes=timeelapsed / 60
						displayminutes=format(minutes, '.2f') 
						sys.stdout.write(str(linecounter)+' total variants processed, last 1M in '+str(displayminutes)+' minutes\n')
						sys.stdout.flush()
						oldtime=newtime
					ll=line.split('\t')
					chroosome=ll[0]
					if 'chr' in chroosome:
						chroosome=chroosome.replace('chr','')
					pos=ll[1]
					ref=ll[3]
					alt=ll[4]
					variant=ref+pos+alt
					if chroosome not in cd:
						cd[chroosome]=[variant]
					elif chroosome in cd:
						cd[chroosome].append(variant)
	newtime=time.time()
	timeelapsed = newtime-starttime
	minutes = timeelapsed / 60
	displayminutes=format(minutes, '.2f') 
	oldtime=newtime
	sys.stdout.write(str(anfile)+' read done in '+str(displayminutes) +' minutes\nNow starting subtraction\n')
	sys.stdout.flush()
	linecounter=0
	if '.gz' in infile[len(infile)-3:]:
		with io.TextIOWrapper(io.BufferedReader(gzip.open(file))) as fh:
			for line in fh:
				if '#' not in line[0]:
					line=line.strip()
					linecounter+=1
					if linecounter % 10000 == 0:
						newtime=time.time()
						timeelapsed = newtime-oldtime
						minutes=timeelapsed / 60 / 60
						displayminutes=format(minutes, '.2f') 
						sys.stdout.write(str(linecounter)+' total variants processed, last 10k in '+str(displayminutes)+' seconds\n')
						sys.stdout.flush()
						oldtime=newtime
					ll = line.split('\t')
					chroosome=ll[0]
					if 'chr' in chroosome:
						chroosome=chroosome.replace('chr','')
					pos=ll[1]
					ref=ll[3]
					alt=ll[4]
					varient=ref+pos+alt
					if chroosome not in cd:
						opt+=line+'\t\n'
					elif varient not in cd[chroosome]:
						opt+=line+'\t\n'
					else:
						opt+=line+'\tX\n'
	else:
		with open(infile) as fh:
			for line in fh:
				if '#' not in line[0]:
					line=line.strip()
					linecounter+=1
					if linecounter % 10000 == 0:
						newtime=time.time()
						timeelapsed = newtime-oldtime
						minutes=timeelapsed / 60 / 60
						displayminutes=format(minutes, '.2f') 
						sys.stdout.write(str(linecounter)+' total variants processed, last 10k in '+str(displayminutes)+' seconds\n')
						sys.stdout.flush()
						oldtime=newtime
					ll = line.split('\t')
					chroosome=ll[0]
					if 'chr' in chroosome:
						chroosome=chroosome.replace('chr','')
					pos=ll[1]
					ref=ll[3]
					alt=ll[4]
					varient=ref+pos+alt
					if chroosome not in cd:
						opt+=line+'\t\n'
					elif varient not in cd[chroosome]:
						opt+=line+'\t\n'
					else:
						opt+=line+'\tX\n'
	with open(outfile,'w') as fh:
		fh.write(opt)
	newtime=time.time()
	timeelapsed = newtime-starttime
	minutes = timeelapsed / 60
	displayminutes=format(minutes, '.2f') 
	sys.stdout.write('total annotation time '+str(displayminutes)+' minutes\n')
	sys.stdout.flush()

if __name__ == '__main__':
	import sys
	vcf_ann(sys.argv[1], sys.argv[2])