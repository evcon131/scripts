def vcf_subtract(file, file2):
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
	if '.gz' in file:
		with io.TextIOWrapper(io.BufferedReader(gzip.open(file))) as fh:
			for line in fh:
				if '#' not in line:
					ll=line.split('\t')
					chroosome=ll[0]
					if 'chr' in chroosome:
						chroosome=chroosome.replace('chr','')
					if chroosome not in cd:
						cd[chroosome]=[ll[1]]
					elif chroosome in cd:
						cd[chroosome].append(ll[1])
	else:
		for line in fh:
			if '#' not in line:
				ll=line.split('\t')
				chroosome=ll[0]
				if 'chr' in chroosome:
					chroosome=chroosome.replace('chr','')
				if chroosome not in cd:
					cd[chroosome]=[ll[1]]
				elif chroosome in cd:
					cd[chroosome].append(ll[1])
	newtime=time.time()
	timeelapsed = newtime-starttime
	minutes = timeelapsed / 60
	displayminutes=format(minutes, '.2f') 
	sys.stdout.write("B Dictionary done in "+str(displayminutes)+" minutes\n")
	sys.stdout.flush()
	oldtime=newtime
	if '.gz' in file2:
		with io.TextIOWrapper(io.BufferedReader(gzip.open(file2))) as fh:
			for line in fh:
				if '#' not in line:
					linecounter+=1
					if linecounter % 100000 == 0:
						newtime=time.time()
						timeelapsed = newtime-oldtime
						minutes=timeelapsed / 60
						displayminutes=format(minutes, '.2f') 
						sys.stdout.write(str(linecounter)+' SNPs processed in '+str(displayminutes)+' minutes\n')
						sys.stdout.flush()
						oldtime=newtime
					ll = line.split('\t')
					chroosome=ll[0]
					if 'chr' in chroosome:
						chroosome=chroosome.replace('chr','')
					if chroosome not in cd:
						opt+=line
					elif ll[1] not in cd[chroosome]:
						opt+=line
	else:
		with open(file2) as fh:
			for line in fh:
				if '#' not in line:
					linecounter+=1
					if linecounter % 100000 == 0:
						newtime=time.time()
						timeelapsed = newtime-oldtime
						minutes=timeelapsed / 60
						displayminutes=format(minutes, '.2f') 
						sys.stdout.write(str(linecounter)+' SNPs processed in '+str(displayminutes)+' minutes\n')
						sys.stdout.flush()
						oldtime=newtime
					ll = line.split('\t')
					if 'chr' in chroosome:
						chroosome=chroosome.replace('chr','')
					if chroosome not in cd:
						opt+=line
					elif ll[1] not in cd[chroosome]:
						opt+=line
	with open('out.vcf','w') as fh:
		fh.write(opt)
	newtime=time.time()
	timeelapsed = newtime-starttime
	minutes = timeelapsed / 60
	displayminutes=format(minutes, '.2f') 
	sys.stdout.write('total run time '+str(displayminutes)+' minutes\n')
	sys.stdout.flush()
if __name__ == '__main__':
	print('Tjis will subtract vcfs A-B, any snps in B that are in A will be removed from A and A is returned')
	file2 = input('What file is your vcf to be A? ')
	import os
	import sys
	file2=file2.strip()
	if not os.path.exists(file2):
		print('Barnacles! File not found, try again')
		sys.exit()
	file = input('What file is your vcf to be B? ')
	file=file.strip()
	if not os.path.exists(file):
		print('Barnacles! File not found, try again')
		sys.exit()
	vcf_subtract(file, file2)


