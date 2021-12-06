def genelist_maker(file):
	import gzip
	import io
	import time
	import sys
	import os
	import glob
	import mygene
	mg = mygene.MyGeneInfo()
	genelist=[]
	out=""
	with open(file) as fh:
		for line in fh:
			ll=line.split('\t')
			geneid=ll[0]
			sub=ll[6]
			for i in range(0,10):
				if str(i) in sub:
					if "UTR" not in sub:
						if geneid not in genelist:
							genelist.append(geneid)
							print(sub)
	for item in genelist:
		out+="\n"+item

	with open("genelist.csv","w") as fh:
		fh.write(out)

if __name__ == '__main__':
	import sys
	genelist_maker(sys.argv[1])


