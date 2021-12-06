def hitlist_effect():
	import gzip
	import io
	import time
	import sys
	import os
	import glob
	hit_list={}
	sys.stdout.write('Shits getting real, making gene hit list\n')
	sys.stdout.flush()
	out=''
	var_effect=[]
	effect_out=''
	with open('t_filter.rdf.csub.selectann.720sub_hpclr..vcf') as fh:
		for line in fh:
			if '#' not in line[0]:
				ll=line.split('\t')
				ll=ll[7].split('|')	
				ann_list=ll[1].split('&')
				if  ll[3] not in hit_list:
					hit_list[ll[3]]={ann_list[0]:0}
				for item in ann_list:
					if item not in var_effect:
						var_effect.append(item)
				for item in ann_list:
					if item not in hit_list[ll[3]]:
						hit_list[ll[3]][item]=1
					elif item in hit_list[ll[3]]:
						hit_list[ll[3]][item]+=1
	for key in hit_list:
		outline=key+','
		for effect in hit_list[key]:
			outline+=effect+','
			outline+=str(hit_list[key][effect])+','
		outline=outline.strip(',')
		outline+='\n'
		out+=outline
		effect_out=var_effect[0]
	for item in var_effect[1:len(var_effect)]:
		effect_out+=','
		effect_out+=item
	with open('hitlist.csv','w') as fh:
		fh.write(out)
	with open('effects.csv','w') as fh:
		fh.write(effect_out)

def hitlist_by_effect():
	import gzip
	import io
	import time
	import sys
	import os
	import glob
	out='symbol'
	elist=[]
	with open('effects.csv') as fh:
		for line in fh:
			ll=line.split(',')
			for item in ll:
				out+=','
				out+=item
				elist.append(item)
	out+=',sum\n'

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
			for item in elist:
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
			out+=outline+'\n'
	with open('hitlist_effect.csv','w') as fh:
		fh.write(out)

def space_fixer(file):
	out=''
	with open(file) as fh:
		for line in fh:
			outline=line.replace('_',' ')
			out+=outline
	with open(file,'w') as fh:
		fh.write(out)

if __name__ == '__main__':
	hitlist_effect()
	hitlist_by_effect()
	space_fixer('hitlist_effect.csv')






