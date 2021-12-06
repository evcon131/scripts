import gzip
import io
import time
import sys
import os
import glob
from statistics import *
out_af='Sample,AF\n'
out_rd='Sample,RD\n'
cout_rd='Sample,RD\n'
cout_af='Sample,AF\n'
linecounter=0
starttime=time.time()
allele_frequewncy_list=[]
read_depth_list= []	
t_list=glob.glob('T*')
c_files=glob.glob('C*')	
for file in t_list:	
	with open(file) as fh:
		cnt=0
		allele_frequewncy_list=[]
		read_depth_list= []	
		for line in fh:
			if '#' not in line[0]:
				ll=line.split('\t')
				cnt+=1
				try:
					ll=ll[9].split(':')	
				except:
					print(ll)
					print(line)
					print(file)
					print(cnt)
				AD=ll[1]
				ll2=AD.split(',')
				read_depth=float(ll2[1])
				if float(ll2[0]) == 0:
					allele_frequewncy=1
				else:
					allele_frequewncy=float(ll2[1])/float(ll2[0])
				allele_frequewncy_list.append(allele_frequewncy)
				read_depth_list.append(read_depth)
		for item in read_depth_list:
			item=str(item)
			out_rd+=file[0:-8]+','
			out_rd+=item+'\n'
		for item in allele_frequewncy_list:
			item=str(item)
			out_af+=file[0:-8]+','
			out_af+=item+'\n'
with open('t_filter.vcf') as fh:
	allele_frequewncy_list=[]
	read_depth_list= []	
	for line in fh:
		if '#' not in line[0]:
			ll=line.split('\t')
			ll=ll[9].split(':')	
			AD=ll[1]
			ll2=AD.split(',')
			read_depth=float(ll2[1])
			if float(ll2[0]) == 0:
				allele_frequewncy=1
			else:
				allele_frequewncy=float(ll2[1])/float(ll2[0])
			allele_frequewncy_list.append(allele_frequewncy)
			read_depth_list.append(read_depth)
	for item in read_depth_list:
		item=str(item)
		out_rd+='t_filter'+','
		out_rd+=item+'\n'
	for item in allele_frequewncy_list:
		item=str(item)
		out_af+='t_filter'+','
		out_af+=item+'\n'
for file in c_files:	
	with open(file) as fh:
		allele_frequewncy_list=[]
		read_depth_list= []	
		for line in fh:
			if '#' not in line[0]:
				ll=line.split('\t')
				ll=ll[9].split(':')	
				AD=ll[1]
				ll2=AD.split(',')
				read_depth=float(ll2[1])
				if float(ll2[0]) == 0:
					allele_frequewncy=1
				else:
					allele_frequewncy=float(ll2[1])/float(ll2[0])
				allele_frequewncy_list.append(allele_frequewncy)
				read_depth_list.append(read_depth)
		for item in read_depth_list:
			item=str(item)
			cout_rd+=file[0:-8]+','
			cout_rd+=item+'\n'
		for item in allele_frequewncy_list:
			item=str(item)
			cout_af+=file[0:-8]+','
			cout_af+=item+'\n'
with open('T_read_depth.csv','w') as fh:
	fh.write(out_rd)
with open('T_af.csv','w') as fh:
	fh.write(out_af)
with open('C_read_depth.csv','w') as fh:
	fh.write(cout_rd)
with open('C_af.csv','w') as fh:
	fh.write(cout_af)

