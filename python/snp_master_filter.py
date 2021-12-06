def lineCounter(file):
	import gzip
	import io
	cnt=0
	if '.gz' in file:
		with io.TextIOWrapper(io.BufferedReader(gzip.open(file))) as fh:
			for line in fh:
				if '#' not in line:
					cnt+=1
	else:
		with open(file) as fh:
			for line in fh:
				if '#' not in line:
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
			for line in fh:
				if '#' not in line[0]:
					ll=line.split('\t')
					ll=ll[7].split('|')
					if ll[5] != 'intergenic_region':
						if ll[7] == 'protein_coding':
							if ll[1] != 'synonymous_variant':
								line=line.strip()
								sample_id=ll[len(ll)-1]
								sample_id=sample_id.strip()
								if "/" in sample_id:
									sample_id_list=sample_id.split("/")
									sample_id=sample_id_list[len(sample_id_list)-1]
								line+='\t'+sample_id+'\n'
								out+=line
								counter+=1
			sys.stdout.write(file+' had '+str(counter)+'\n')
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
				ll=line.split('\t')
				ll=ll[9].split(':')	
				AD=ll[1]
				ll2=AD.split(',')
				read_depth=float(ll2[1])
				read_depth_list.append(read_depth)
	read_depth_median=median(read_depth_list)
	return read_depth_median

def RD_filter(file):
	rd_cutoff=read_depth_median('t_filter.vcf')
	out=''
	sys.stdout.write('Starting read depth filter\n')
	sys.stdout.flush()
	with open(file) as fh:
		for line in fh:
			if '#' not in line[0]:
				ll=line.split('\t')
				ll=ll[9].split(':')	
				AD=ll[1]
				ll2=AD.split(',')
				read_depth=float(ll2[1])
				if read_depth >= rd_cutoff:
					out+=line
	with open('t_filter.rdf.vcf','w') as fh:
		fh.write(out)
	sys.stdout.write('Fuck yeah! Read depth filter done\n')
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
				if ('missense_variant' or 'disruptive_inframe_deletion' or 'frameshift_variant' or 'stop_gained' or 'disruptive_inframe_insertion' or 'exon_loss_variant' or 'disruptive_inframe_deletion' or 'start_loss' or 'stop_loss') in ll[1]:
					out+=line

	with open('t_filter.rdf.csub.selectann.vcf','w') as fh:
		fh.write(out)
	sys.stdout.write('OK done with the fucking function buisness\n')
	sys.stdout.flush()

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
	else:
		with open(file2) as fh:
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
					chroosome=ll[0]
					if 'chr' in chroosome:
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
					if 'chr' in chroosome:
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
	with open('t_filter.rdf.csub.selectann.720sub.vcf') as fh:
		for line in fh:
			if '#' not in line[0]:
				ll=line.split("\t")
				sample_id=ll[len(ll)-1]
				sample_id=sample_id.strip()
				if "/" in sample_id:
					sample_id_list=sample_id.split("/")
					sample_id=sample_id_list[len(sample_id_list)-1]
				ll=ll[7].split('|')	
				if  ll[3] not in hit_list:
					hit_list[ll[3]]={sample_id:1}
				elif ll[3] in hit_list:
					if sample_id not in hit_list[ll[3]]:
						hit_list[ll[3]][sample_id]=1
					elif sample_id in hit_list[ll[3]]:
						hit_list[ll[3]][sample_id]+=1
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
	outline+='sum'
	out+=outline+'\n'

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
			out+=outline+'\n'
	with open('hitlist_bysample.csv','w') as fh:
		fh.write(out)

def snp_summary():
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
	report+='Total starting snps combining all files and requiring varients be in a protein coding gene: '+str(starting)+'\n'
	step2=lineCounter('t_filter.rdf.vcf')
	loss=starting-step2
	report+=str(loss)+' snps lost when requiring read depth '+str(read_depth_median('t_filter.vcf'))+' '+str(step2)+' remaining\n'
	step3=lineCounter('t_filter.rdf.csub.vcf')
	loss=step2-step3
	report+=str(loss)+' snps lost when comparing controls '+str(step3)+'remaining\n'
	step4=lineCounter('t_filter.rdf.csub.selectann.vcf')
	loss=step4-step3
	report+=str(loss)+' snps lost when filtering on requiring functional changes '+str(step4)+'remaining\n'
	step5=lineCounter('t_filter.rdf.csub.selectann.vcf')
	loss=step5-step4
	report+=str(loss)+' snps lost when filtering out dog reference database(722g.990.SNP.INDEL.chrAll.vcf.gz) '+str(step5)+'remaining\n'
	rd_cutoff=read_depth_median('t_filter.vcf')
	report+='The read depth median of t_filter.vcf was '+str(rd_cutoff)+'\n'
	report+='For snps to pass they has to habe greater than or equal to that\n'
	with open('Results_summary.txt','w') as fh:
		fh.write(report)
	steps=['Initial merge\nprotein coding','Read\nDepth','Control\nFilter','Functional\nVarients', 'Dog SNP\nDatabase']
	values=[starting,step2,step3,step4,step5]
	plt.plot(steps,values,color='purple',marker='o')
	plt.ylabel('SNPs')
	plt.title('SNP Survival')
	for x,y in zip(steps,values):
		label = y
		plt.annotate(label, 
			(x,y), # this is the point to label
			textcoords="offset points", # how to position the text
			xytext=(2,2), # distance from text to points (x,y)
			ha='left') # horizontal alignment can be left, right or center

	plt.savefig('SNP_survival_plot.pdf')

def snp_tidy():
	import os
	os.mkdir('final_results')
	os.rename('SNP_survival_plot.pdf','final_results/SNP_survival_plot.pdf')
	os.rename('hitlist_bysample.csv','final_results/hitlist_bysample.csv')
	os.rename('Results_summary.txt','final_results/Results_summary.txt')
	os.rename('t_filter.rdf.csub.selectann.vcf','final_results/t_filter.rdf.csub.selectann.vcf')

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
		control_id=input('Alrighty then, whats your control filr id or list>? ')
		if '.list' in control_id:
			with open(control_id) as fh:
				for line in fh:
					line=line.atrip()
					control_file_list.append(line)
		else:
			control_file_list=glob.glob(control_id+'*')
		print('My wizard powers say your conytol files are:')
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
	vcf_subtract('t_filter.rdf.csub.selectann.vcf','/lab_data/avery_lab/reference_files/722g.990.SNP.INDEL.chrAll.vcf.gz', 't_filter.rdf.csub.selectann.720sub.vcf')
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
	hitlist_maker()
	hitlist_by_sample()
	snp_summary()
	snp_tidy()
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

