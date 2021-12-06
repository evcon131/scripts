def vcf_condensor(file):
	import gzip
	import io
	import time
	import sys
	import os
	import glob
	import mygene
	mg = mygene.MyGeneInfo()
	slist=[]
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
				geneid=ll[7]
				transcript=ll[9]
				sub=ll[12]
				sub=sub.replace("p.","")
				if sub=="":
					sub=ll[11]
				symbol=ll[8]
				dkey=geneid+'\t'+symbol+'\t'+transcript+'\t'+chromosome+'\t'+pos+'\t'+ref+'\t'+alt+'\t'+sub
				if dkey not in refd:
					refd[dkey]=[sample_id]
				elif sample_id not in refd[dkey]:
					refd[dkey].append(sample_id)
				if sample_id not in slist:
					slist.append(sample_id)
	out='geneid\tsymbol\ttranscript_ID\tchr\tpos\tref\talt\tAA sub\tnumber samples containing'
	for item in slist:
		out+='\t'+item
	out+='\n'

	for key in refd:
		outline=key
		outline+='\t'+str(len(refd[key]))
		for item in slist:
			if item in refd[key]:
				outline+='\tX'
			else:
				outline+='\t'
		outline+='\n'
		out+=outline

	with open('condensd_vcf.tab','w') as fh:
		fh.write(out)

if __name__ == '__main__':
	import sys
	vcf_condensor(sys.argv[1])

