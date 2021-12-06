def merge_vcf_dict(prefix):
	import glob
	merge_dict={}
	file_list=glob.glob(prefix+'*')
	for file in file_list:
		with open(file) as fh:
			for line in fh:
				ll = line.split('\t')
				chromosome=ll[0].replace('chr','')
				pos=ll[1]
				huh=ll[2]
				ref=ll[3]
				alt=ll[4]
				variant=chromosome+'\t'+pos+'\t'+huh+'\t'+ref+'\t'+alt
				if variant not in merge_dict:
					merge_dict[variant]=[ll[10]]
					merge_dict[variant].append(ll[11])
				elif variant in merge_dict:
					merge_dict[variant].append(ll[10])
					merge_dict[variant].append(ll[11])
	return merge_dict
	
def write_out(merge_d,outf='out.vcf'):
	for key in merge_d:
		outl=key
		outl+=';'+'\t'+'\t'+'\t'+'\t'
		for item in merge_d[key]:
			outl+='\t'+item
		with open(outf, 'a') as fh:
			fh.write(outl)

if __name__ == '__main__':
	import sys
	merged=merge_vcf_dict(sys.argv[1])				
	write_out(merged)