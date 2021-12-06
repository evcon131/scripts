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
file_counter=0
starttime=time.time()
sys.stdout.write('starting control files...\n')
sys.stdout.flush()
for file in control_file_list:
	if '.gz' in file:
		with io.TextIOWrapper(io.BufferedReader(gzip.open(file))) as fh:
			for line in fh:
				if '#' not in line[0]:
					ll=line.split('\t')
					ll=ll[7].split('|')
					cnter=0
					for item in ll:
						if 'ENSCAFG' in item:
							if cnter==0:
								if item not in control_gene_list:
									control_gene_list.append(item)
									cnter=1000
	else:
		with open(file) as fh:
			for line in fh:
				if '#' not in line[0]:
					ll=line.split('\t')
					ll=ll[7].split('|')
					cnter=0
					for item in ll:
						if 'ENSCAFG' in item:
							if cnter==0:
								if item not in control_gene_list:
									control_gene_list.append(item)
									cnter=1000
elapsedtime=time.time() - starttime
if elapsedtime > 60:
	minutes= elapsedtime / 60
	displayminutes=format(minutes, '.2f') 
	sys.stdout.write('controls ran in: ' + str(displayminutes) + ' minutes\n')
	sys.stdout.flush()
else:
	displayseconds=format(elapsedtime, '.2f') 
	sys.stdout.write('controls ran in: ' + str(displayseconds) + ' seconds\n')
	sys.stdout.flush()
for file in tumor_file_list:
	if '.gz' in file:
		with io.TextIOWrapper(io.BufferedReader(gzip.open(file))) as fh:
			snp_counter=0
			for line in fh:
				if '#' not in line[0]:
					ll=line.split('\t')
					ll=ll[7].split('|')
					cnter=0
					for item in ll:
						if 'ENSCAFG' in item:
							if cnter==0:
								if item not in control_gene_list:
									out+=line.strip()+'\t'+file[0:-11]+'\n'
									snp_counter+=1
									cnter=1000
			sys.stdout.write(file+' had ' + str(snp_counter)+ ' SNPs written\n')
			sys.stdout.flush()
	else:
		with open(file) as fh:
			snp_counter=0
			for line in fh:
				if '#' not in line[0]:
					ll=line.split('\t')
					ll=ll[7].split('|')
					cnter=0
					for item in ll:
						if 'ENSCAFG' in item:
							if cnter==0:
								if item not in control_gene_list:
									out+=line.strip()+'\t'+file[0:-8]+'\n'
									snp_counter+=1
									cnter=1000
			sys.stdout.write(file+' had ' + str(snp_counter)+ ' SNPs written\n')
			sys.stdout.flush()

with open('t_unique.vcf','w') as fh:
	fh.write(out)
elapsedtime=time.time() - starttime
if elapsedtime > 60:
	minutes= elapsedtime / 60
	displayminutes=format(minutes, '.2f') 
	print('Total run time: ' + str(displayminutes) + ' minutes')
else:
	print('Total run time: ' + str(elapsedtime) + ' seconds')



