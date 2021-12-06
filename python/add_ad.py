def AD_dict_maker(infile):
	import gzip
	import io
	import time
	import sys
	import os
	import glob
	ad_dict={}
	with open(infile) as fh:
		for line in fh:
			if '#' not in line[0]:
				ll=line.split("\t")
				if 'chr' in ll[0]:
					chromosome=ll[0].replace('chr', '')
				else:
					chromosome=ll[0]
				pos=ll[1]
				ref=ll[3]
				alt=ll[4]
				variant=ref+pos+alt
				for i in range(9,14):
					ann=ll[i]
					ad=ann.split(':')[1]
					if variant not in ad_dict:
						ad_dict[variant]=[ad]
					else:
						ad_dict[variant].append(ad)
		return ad_dict

def add_cotrol_add(infile, cfile, outfile):
	out=''
	ad_dict=AD_dict_maker(cfile)
	with open(infile) as fh:
		for line in fh:
			if '#' not in line[0]:
				ll=line.split("\t")
				line=line.strip()
				if 'chr' in ll[0]:
					chromosome=ll[0].replace('chr', '')
				else:
					chromosome=ll[0]
				pos=ll[1]
				ref=ll[3]
				alt=ll[4]
				variant=ref+pos+alt
				if variant in ad_dict:
					for ad in ad_dict[variant]:
						line+='\t'
						ad=ad.split(',')
						line+=ad[0]+'\t'
						line+=ad[1]
				else:
					line+='\t'*10
				line+='\n'
				out+=line
	with open(outfile, 'w') as fh:
		fh.write(out)

if __name__ == '__main__':
	import sys
	add_cotrol_add(sys.argv[1], sys.argv[2], sys.argv[3])

			


