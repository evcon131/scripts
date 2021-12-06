def vcf_finder_variant_type_number(file):
	import gzip
	import io
	import time
	import sys
	import os
	import glob
	import mygene
	import matplotlib.pyplot as plt; plt.rcdefaults()
	import numpy as np
	import matplotlib.pyplot as plt
	from pylab import rcParams
	rcParams['figure.figsize'] = 50, 15
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
				for i in range(1,len(ll)-6,15):
					variant_type=ll[i]
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
	plt.clf()
	y_pos = np.arange(len(var_type))
	plt.barh(y_pos, var_nums, color="cornflowerblue")
	plt.yticks(y_pos, var_type)
	plt.xlabel('Number Variants')
	plt.title('Variant Type')
	for index, value in enumerate(var_nums):
		plt.text(value, index, str(value), fontsize=8)
	plt.savefig("varianttype_bar.pdf")
if __name__ == '__main__':
	import sys
	vcf_finder_variant_type_number(sys.argv[1])

