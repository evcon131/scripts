def lollipops_maker(file):
	import gzip
	import io
	import time
	import sys
	import os
	import glob
	import mygene
	mg = mygene.MyGeneInfo()
	out='!# /bin/bash\nmkdir lollipop_plots\ncd lollipop_plots\n'
	lollid={}
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
				sub=ll[10]
				sub=sub.replace('p.','')
				try:
					symd=mg.getgene(geneid, fields='symbol')
					sym=symd['symbol']
					gene=sym
				except:
					gene=geneid
				lolikey=gene
				if lolikey not in lollid:
					lollid[lolikey]=[sub]
				elif sub not in lollid[lolikey]:
					lollid[lolikey].append(sub)

	for key in lollid:
		out+='lollipops -labels -legend '
		out+=key
		for aasub in lollid[key]:
			out+=' '+aasub
		out+='\n'
	
	for key in lollid:
		out+='magick convert '+key+'.svg '+key+'.pdf\n'
	out+='mkdir pdf\nmkdir svg\nmv *.svg svg/\nmv *.pdf pdf/'

	with open('lollipops.sh','w') as fh:
		fh.write(out)

	os.chmod('lollipops.sh',0o777)

if __name__ == '__main__':
	import sys
	lollipops_maker(sys.argv[1])



