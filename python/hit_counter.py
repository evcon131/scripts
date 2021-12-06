import gzip
import io
import time
import sys
import os
import glob
hit_list={}
out=''
with open('t_filter.720sub.csub.selectann.af_rd.vcf') as fh:
	for line in fh:
		if '#' not in line[0]:
			ll=line.split('\t')
			sample_id=ll[len(ll)-1]
			sample_id=sample_id.strip()
			ll=ll[7].split('|')	
			if  ll[3] not in hit_list:
				hit_list[ll[3]]={sample_id:1}
			elif ll[3] in hit_list:
				if sample_id not in hit_list[ll[3]]:
					hit_list[ll[3]][sample_id]=1
				elif sample_id in hit_list[ll[3]]:
					hit_list[ll[3]][sample_id]+=1
for key in hit_list:
	out+=key+','
	for sampled in hit_list[key]:
		out+=sampled+','
		out+=str(hit_list[key][sampled])+','
	out+='\n'
with open('hitlist.csv','w') as fh:
	fh.write(out)

