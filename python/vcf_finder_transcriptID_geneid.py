def vcf_finder_transid_geneid(file, qgeneid):
	import gzip
	import io
	import time
	import sys
	import os
	import glob
	import mygene
	mg = mygene.MyGeneInfo()
	outd={}
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
				geneid=ll[4]
				if geneid == qgeneid:
					for  item in ll:
						if "ENSCAFT" in item:
							transid=item
							if transid not in outd:
								outd[transid]=1
							elif transid in outd:
								outd[transid]+=1
	for key in outd:
		print(key+' '+str(outd[key]))
if __name__ == '__main__':
	import sys
	vcf_finder_transid_geneid(sys.argv[1], sys.argv[2])
