def lineCounter(file):
	import gzip
	import io
	cnt=0
	if '.gz' in file[len(file)-3:]:
		with io.TextIOWrapper(io.BufferedReader(gzip.open(file))) as fh:
			for line in fh:
				if '#' not in line[0]:
					cnt+=1
	else:
		with open(file) as fh:
			for line in fh:
				if '#' not in line[0]:
					cnt+=1
	return cnt

def filter(tumor_id='T'):
	import gzip
	import io
	import time
	import sys
	import os
	import glob
	sys.stdout.write('Starting File merge\n')
	sys.stdout.flush()
	if '.list' in tumor_id:
		with open(tumor_id) as fh:
			for line in fh:
				tfile=line.strip()
				tumor_file_list.apprnd(tfile)
	else:
		tumor_file_list=glob.glob(tumor_id+'*')	
	out=''
	counter=0
	starttime=time.time()
	for file in tumor_file_list:
		with open(file) as fh:
			counter=0
			if "/" in file:
				sample_id_list=file.split("/")
				sample_id=sample_id_list[len(sample_id_list)-1]
				sample_id=sample_id[0:-11]
			else:
				sample_id=file[0:-11]
			for line in fh:
				if '#' not in line[0]:
					ll=line.split('\t')
					quality=ll[5]
					try:
						quality=float(quality)
					except:
						quality=0
					ll=ll[7].split('|')
					if 'protein_coding' in ll:
						if quality > 40:
							line=line.strip()
							line+='\t'+sample_id+'\n'
							out+=line
							counter+=1
			sys.stdout.write(file+' had '+str(counter)+'\n')
			sys.stdout.flush()
	sys.stdout.write('Writing t_filter.vcf...\n')
	sys.stdout.flush()
	with open('t_filter.vcf','w') as fh:
		fh.write(out)
	sys.stdout.write('File merge donezo\n')
	sys.stdout.flush()

def read_depth_median(file):
	import gzip
	import io
	import time
	import sys
	import os
	from statistics import median
	opt=''
	linecounter=0
	starttime=time.time()
	read_depth_list=[]
	with open(file) as fh:
		for line in fh:
			if '#' not in line[0]:
				index=0
				ad_index_l=ll[8].split(':')
				for item in ad_index_l:
					index+=1
					if item == 'DP':
						vardepth_index=index
				adll=ll[9].split(':')
				AD=adll[AD_index]
				ll2=AD.split(',')
				WT_depth=ll2[0]
				vardepth=adll[vardepth_index]
				read_depth=float(vardepth)
				read_depth_list.append(read_depth)
	read_depth_median=median(read_depth_list)
	return read_depth_median

def RD_filter(file):
	import gzip
	import io
	import time
	import sys
	import os
	sys.stdout.write('Starting read depth filter\n')
	sys.stdout.flush()
	rd_cutoff=read_depth_median(file)
	out=''
	with open(file) as fh:
		for line in fh:
			if '#' not in line[0]:
				index=-1
				ll=line.split('\t')
				ad_index_l=ll[8].split(':')
				for item in ad_index_l:
					index+=1
					if item =="AD":
						AD_index=index
				ll=ll[9].split(':')
				AD=ll[AD_index]
				ll2=AD.split(',')
				read_depth=float(ll2[1])
				if read_depth >= rd_cutoff:
					out+=line
	with open('t_filter.rdf.vcf','w') as fh:
		fh.write(out)
	sys.stdout.write('The median read depth was '+str(rd_cutoff)+ '\nFuck yeah! Read depth filter done\n')
	sys.stdout.flush()


def control_subtractor(control_id='C'):
	import gzip
	import io
	import time
	import sys
	import os
	import glob
	control_file_list=[]
	if '.list' in control_id:
		with open(control_id) as fh:
			for line in fh:
				cfile=line.strip()
				control_file_list.apprnd(cfile)
	else:
		control_file_list=glob.glob(control_id+'*')
	out=''
	cd = {}
	counter=0
	starttime=time.time()
	sys.stdout.write('Starting control subtraction\n')
	sys.stdout.flush()
	for file in control_file_list:
		with open(file) as fh:
			for line in fh:
				if '#' not in line:
					ll=line.split('\t')
					pos=ll[1]
					ref=ll[3]
					alt=ll[4]
					varient=ref+pos+alt
					if ll[0] not in cd:
						cd[ll[0]]=[varient]
					if ll[0] in cd:
						cd[ll[0]].append(varient)

	with open('t_filter.rdf.vcf') as fh:
		for line in fh:
			if '#' not in line:
				ll = line.split('\t')
				pos=ll[1]
				ref=ll[3]
				alt=ll[4]
				varient=ref+pos+alt
				if ll[0] not in cd:
					out+=line
				elif ll[0] in cd:
					if varient not in cd[ll[0]]:
						out+=line
	with open('t_filter.rdf.csub.vcf', 'w') as fh:
		fh.write(out)
	sys.stdout.write('Shits yeah! Moving on!\n')
	sys.stdout.flush()


def func_ann_select():
	import gzip
	import io
	import time
	import sys
	import os
	import glob
	outputd={}
	out=''
	sys.stdout.write('Starting functional annotation filter\n')
	sys.stdout.flush()
	with open('t_filter.rdf.csub.vcf') as fh:
		for line in fh:
			if '#' not in line[0]:
				ll=line.split('\t')
				ll=ll[7].split('|')	
				if ("HIGH" or "MODERATE") in ll:
					out+=line
	with open('t_filter.rdf.csub.selectann.vcf','w') as fh: 
		fh.write(out)
	sys.stdout.write('OK done with the fucking function buisness\n')
	sys.stdout.flush()

def hitlist_maker():
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
	with open('t_filter.rdf.csub.selectann.720esub.vcf') as fh:
		for line in fh:
			if '#' not in line[0]:
				ll=line.split("\t")
				sample_id=ll[len(ll)-1]
				sample_id=sample_id.strip()
				if "/" in sample_id:
					sample_id_list=sample_id.split("/")
					sample_id=sample_id_list[len(sample_id_list)-1]
				nll=ll[7].split('|')	
				if  nll[4] not in hit_list:
					hit_list[nll[4]]={sample_id:1}
				elif nll[4] in hit_list:
					if sample_id not in hit_list[nll[4]]:
						hit_list[nll[4]][sample_id]=1
					elif sample_id in hit_list[nll[4]]:
						hit_list[nll[4]][sample_id]+=1
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

def variant_summary():
	import gzip
	import io
	import time
	import sys
	import os
	import glob
	import matplotlib.pyplot as plt
	import matplotlib.path as mpath
	import numpy as np
	sys.stdout.write('Thank fucking god last step, making Summary Files\n')
	sys.stdout.flush()	
	report=''
	starting=lineCounter('t_filter.vcf')
	report+='Total starting variants combining all files and requiring variants be in a protein coding gene: '+str(starting)+'\n'
	step2=lineCounter('t_filter.rdf.vcf')
	loss=starting-step2
	report+=str(loss)+' variants lost when requiring read depth '+str(read_depth_median('t_filter.vcf'))+', '+str(step2)+' remaining\n'
	step3=lineCounter('t_filter.rdf.csub.vcf')
	loss=step2-step3
	report+=str(loss)+' variants lost when comparing controls '+str(step3)+' remaining\n'
	step4=lineCounter('t_filter.rdf.csub.selectann.vcf')
	loss=step3-step4
	report+=str(loss)+' variants lost when filtering on requiring functional changes '+str(step4)+' remaining\n'
	step5=lineCounter('t_filter.rdf.csub.selectann.720esub.vcf')
	loss=step4-step5
	report+=str(loss)+' variants lost when filtering out dog reference database(722g.990.SNP.INDEL.chrAll.vcf.gz) and ensemble reference(canis_lupus_familiaris.vcf) '+str(step5)+' remaining\n'
	rd_cutoff=read_depth_median('t_filter.vcf')
	report+='The read depth median of t_filter.vcf was '+str(rd_cutoff)+'\n'
	report+='For variants to pass they must have greater than or equal to that\n'
	with open('results_summary.txt','w') as fh:
		fh.write(report)
	steps=['Initial merge\nprotein coding','Read\nDepth','Control\nFilter','Functional\nVarients', 'Dog variants\nDatabases']
	values=[starting,step2,step3,step4,step5]
	plt.plot(steps,values,color='purple',marker='o')
	plt.ylabel('Variants')
	plt.title('Variant Survival')
for x,y in zip(x,y):
	label = y
	plt.annotate(label, 
		(x,y), # this is the point to label
		textcoords="offset points", # how to position the text
		xytext=(2,2), # distance from text to points (x,y)
		ha='left') # horizontal alignment can be left, right or center

	plt.savefig('variant_survival_plot.pdf')

def variant_tidy():
	import os
	out_d='final_results'
	if os.path.exists(out_d):
		i=0
		while os.path.exists(out_d):
			i+=1
			out_d=out_d+str(i)
	os.mkdir(out_d)
	os.rename('variant_survival_plot.pdf',out_d+'/variant_survival_plot.pdf')
	os.rename('hitlist_bysample.csv',out_d+'/hitlist_bysample.csv')
	os.rename('results_summary.txt',out_d+'/results_summary.txt')
	os.rename('t_filter.rdf.csub.selectann.720esub.vcf',out_d+'/t_filter.rdf.csub.selectann.720esub.vcf')

if __name__ == '__main__':
	import time
	import sys
	import glob
	answer=''
	starttime=time.time()
	while answer.upper() != 'Y':
		tumor_file_list=[]
		tumor_id=input('Whats your tumor file list or unique prefix? ')
		if '.list' in tumor_id:
			with open(tumor_id) as fh:
				for line in fh:
					line=line.atrip()
					tumor_file_list.append(line)
		else:
			tumor_file_list=glob.glob(tumor_id+'*')
		print('Ok my psychic powers tell me your tumor vcfs are: ')
		for file in tumor_file_list:
			print(file)
		answer=input('Am I right or a fucking fraud?(y/n) ')
	answer=''
	while answer.upper() != 'Y':
		control_file_list=[]
		control_id=input('Alrighty then, whats your control file id or list? ')
		if '.list' in control_id:
			with open(control_id) as fh:
				for line in fh:
					line=line.atrip()
					control_file_list.append(line)
		else:
			control_file_list=glob.glob(control_id+'*')
		print('My wizard powers say your control files are:')
		for file in control_file_list:
			print(file)
		answer=input('So am I right or just a fucking muggle?(y/n) ')
	filter(tumor_id)
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
	RD_filter('t_filter.vcf')
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
	control_subtractor(control_id)
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
	func_ann_select()
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
	sys.stdout.write('Ok this next step is a bitch and might take a while, so nows a good time for coffee\n')
	sys.stdout.flush()
	vcf_subtract('t_filter.rdf.csub.selectann.vcf','/lab_data/avery_lab/reference_files/722g.990.SNP.INDEL.chrAll.vcf.gz.idx', 't_filter.rdf.csub.selectann.720sub.vcf')
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
	sys.stdout.write('Moving on to ensembl variant database...\n')
	sys.stdout.flush()
	vcf_subtract('t_filter.rdf.csub.selectann.720sub.vcf','/lab_data/avery_lab/reference_files/canis_lupus_familiaris.vcf', 't_filter.rdf.csub.selectann.720esub.vcf')
	hitlist_maker()
	hitlist_by_sample()
	variant_summary()
	variant_tidy()
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



