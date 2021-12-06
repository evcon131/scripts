out=''
with open('tznvnewcontrols_dsq_with_snps.csv') as fh:
	out=fh.readline()
	out=out.strip()
	out+=','+'in samples\n'
	for line in fh:
		ll=line.split(',')
		yotal=0
		for item in ll[28:34]:
			if float(item) > 0:
				yotal+=1
		out+=line.strip()+','+str(yotal)+'\n'
with open('tznvnewcontrols_dsq_with_snps.csv','w') as fh: 
	fh.write(out)