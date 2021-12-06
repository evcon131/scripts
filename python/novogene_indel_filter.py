def novogene_indel_filter(prefix):
	import sys
	import glob
	file_list=glob.glob(prefix+"*")
	counter=0
	for file in file_list:
		with open(file) as fh:
			for line in fh:
				if '#' not in line[0]:
					ll=line.split('\t')
					if ll[10]=="protein_coding":
						if ll[13]!="intron_variant":
							line=line.strip()
							line+='\t'+file[0:-17]+'\n'
							out+=line
							counter+=1
	sys.stdout.write(file+' had '+str(counter)+'\n')
	sys.stdout.flush()
	with open('t_indel_filter.vcf','w') as fh:
		fh.write(out)

	if __name__ == '__main__':
		import sys
		novogene_indel_filter(sys.argv[1])			