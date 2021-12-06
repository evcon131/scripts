def hitlist_maker(infile):
	import gzip
	import io
	import time
	import sys
	import os
	import glob
	hit_list={}
	out=''
	sys.stdout.write('Shits getting real, making gene hit list\n')
	sys.stdout.flush()
	with open(infile) as fh:
		for line in fh:
			if '#' not in line[0]:
				ll=line.split("\t")
				sample_id=ll[len(ll)-1]
				sample_id=sample_id.strip()
				if "/" in sample_id:
					sample_id_list=sample_id.split("/")
					sample_id=sample_id_list[len(sample_id_list)-1]
				if  ll[7] not in hit_list:
					hit_list[ll[7]]={sample_id:1}
				elif ll[7] in hit_list:
					if sample_id not in hit_list[ll[7]]:
						hit_list[ll[7]][sample_id]=1
					elif sample_id in hit_list[ll[7]]:
						hit_list[ll[7]][sample_id]+=1
	for key in hit_list:
		out+=key
		for sampled in hit_list[key]:
			out+=','+sampled
			out+=','+str(hit_list[key][sampled])
		out+='\n'
	with open('hitlist.csv','w') as fh:
		fh.write(out)

def hitlist_by_sample():
	import gzip
	import io
	import time
	import sys
	import os
	import glob
	import mygene
	mg = mygene.MyGeneInfo()
	out='symbol,'
	sample_list=[]
	outline=''
	with open('hitlist.csv') as fh:
		for line in fh:
			ll=line.split(',')
			for i in range(1,len(ll),2):
				if ll[i] not in sample_list:
					sample_list.append(ll[i])
	for item in sample_list:
		outline+=item+','
	outline+='sum,symbol/eid'
	out+=outline+'\n'
	sys.stdout.write('Converting ensembl IDs to symbols, might be a bit\n')
	sys.stdout.flush()
	with open('hitlist.csv') as fh:
		for line in fh:
			line=line.strip()
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
			total=0
			for item in snp_counter_list:
				outline+=item+','
			for item in snp_counter_list:
				item=float(item)
				total+=item
			outline+=str(total)
			try:	
					symd=mg.getgene(ll[0], fields='symbol')
					sym=symd['symbol']
					outline+=','+sym
			except:
					outline+=','+ll[0]
			out+=outline+'\n'
	with open('hitlist_bysample.csv','w') as fh:
		fh.write(out)

if __name__ == '__main__':
	import sys
	hitlist_maker(sys.argv[1])
	hitlist_by_sample()
