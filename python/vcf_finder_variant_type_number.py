def vcf_finder_variant_type_number(file):
	import gzip
	import io
	import time
	import sys
	import os
	import glob
	import mygene
	import matplotlib.pyplot as plt
	var_type=[]
	var_nums=[]
	mg = mygene.MyGeneInfo()
	out=''
	refd={}
	with open(file) as fh:
		for line in fh:
			if '#' not in line[0]:
				ll=line.split('\t')
				sample_id=ll[len(ll)-1]
				sample_id=sample_id.strip()
				chromosome=ll[0]
				pos=ll[1]
				ref=ll[3]
				alt=ll[4]
				ll=ll[7].split('|')	
				variant_type=ll[1]
				if variant_type not in refd:
					refd[variant_type]=1
				else:
					refd[variant_type]+=1
	#for key in refd:
	#	print(key)
	#	print(str(refd[key]))
	for key in refd:
		var_type.append(key)
		var_nums.append(refd[key])
	fig = plt.figure()
	ax = fig.add_axes([0,0,1,1])
	ax.bar(var_nums,var_nums)
	plt.show()
if __name__ == '__main__':
	import sys
	vcf_finder_variant_type_number(sys.argv[1])
