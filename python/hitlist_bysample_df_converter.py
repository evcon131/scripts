import gzip
import io
import time
import sys
import os
import glob
out='symbol,'
sample_list=[]
outline=''
with open('hitlist.csv') as fh:
	for line in fh:
		ll=line.split(',')
		for item in ll:
			if 'TZL' in item:
				if item not in sample_list:
					sample_list.append(item)
for item in sample_list:
	outline+=item+','

outline=outline.strip(',')
out+=outline+'\n'

with open('hitlist.csv') as fh:
	for line in fh:
		line=line.strip()
		line=line.strip(',')
		ll=line.split(',')
		out += ll[0]+','
		line_dict={}
		outline=''
		for i in range(1,len(ll),2):
			line_dict[ll[i]]=ll[i+1]
		snp_counter_list=[]
		for item in sample_list:
			if item in line_dict:
				snp_counter_list.append(line_dict[item])
			if item not in line_dict:
				snp_counter_list.append(str(0))
		for item in snp_counter_list:
			outline+=item+','
		outline=outline.strip(',')
		out+=outline+'\n'
with open('hitlist_bysample.csv','w') as fh:
	fh.write(out)


