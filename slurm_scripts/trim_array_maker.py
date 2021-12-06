import glob
out=''
fqs=glob.glob('*1.fq.gz')
for file in fqs:
	newn=file[0:-7]
	out+=newn+'\n'
with open('slm_list.txt','w') as fh:
	fh.write(out)
