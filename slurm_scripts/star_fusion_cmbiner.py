def reader():
	cnt=0
	import glob 
	cfh=glob.glob('c/*')
	tfh=glob.glob('t/*')
	cl=[]
	for fh in cfh:
		with open(fh) as nfh:
			for line in nfh:
				ll=line.split('\t')
				if len(ll) >1:
					item=ll[0]
					if item not in cl:
						cl.append(item)
	out=''
	d2=[]
	refd={}
	d={}
	for fh in tfh:
		with open(fh) as nfh:
			for line in nfh:
				ll=line.split('\t')
				if len(ll) >1:
					item=ll[0]
					if item in d:
						d[item]+=1
						refd[item]+='\t'+fh[2:len(fh)-4]
					if item not in d:
						d[item]=1
						refd[item]='\t'+fh[2:len(fh)-4]

	for fh in tfh:
		with open(fh) as nfh:
			for line in nfh:
				line=line.strip()
				ll=line.split('\t')
				if len(ll) >1:
					item=ll[0]
					if item not in cl:
						if 'INFRAME' in line:
							if ll[0] not in d2:
								d2.append(ll[0])
								out+=line
								cnt+=1
								out+='\t'+str(d[item])+'\t'+refd[item]+'\n'
	with open('out.tsv','w') as ofh:
		ofh.write(out)
if __name__=='__main__':
	reader()


