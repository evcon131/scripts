def merge_vcf_csv_withad(vfile, cfile, outf='out.vcf.csv'):
	import glob
	import time
	import numpy as np
	c_dict={}
	merge_dict={}
	out=''
	with open(cfile) as fh:
		for line in fh:
			if len(line) > 5:
				line=line.strip()
				ll = line.split(';')
				chromosome=ll[0].replace('chr','')
				try:
					pos=ll[1]
				except:
					print(line)
				huh=ll[2]
				ref=ll[3]
				alt=ll[4]
				variant=chromosome+';'+pos+';'+huh+';'+ref+';'+alt
				ad=ll[10:len(ll)]
				c_dict[variant]=ad
	with open(vfile) as fh:
		for line in fh:
			if len(line) > 5:
				line=line.strip()
				ll = line.split(';')
				chromosome=ll[0].replace('chr','')
				pos=ll[1]
				huh=ll[2]
				ref=ll[3]
				alt=ll[4]
				variant=chromosome+';'+pos+';'+huh+';'+ref+';'+alt
				merge_dict[variant]=(ll[10:len(ll)])
	for key in merge_dict:
		if key in c_dict:
			merge_dict[key]=np.concatenate([merge_dict[key], c_dict[key]])
	for key in merge_dict:
		outl=key
		outl+=';'+';'+';'+';'+';'
		for item in merge_dict[key]:
			outl+=';'+str(item)
		outl+='\n'
		out+=outl
	with open(outf, 'w') as fh:
		fh.write(out)

if __name__ == '__main__':
	import sys
	merge_vcf_csv_withad(sys.argv[1], sys.argv[2])	

