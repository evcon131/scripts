def WT_depth_printer_whole_file(file):
	import gzip
	import io
	import time
	import sys
	import os
	from statistics import median
	opt=''
	linecounter=0
	starttime=time.time()
	WT_list=[]
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
				WT_depth=float(ll2[0])
				if WT_depth not in WT_list:
					WT_list.append(WT_depth)
	for item in WT_list:
		print(str(item))

if __name__ == '__main__':
	import sys
	WT_depth_printer_whole_file(sys.argv[1])