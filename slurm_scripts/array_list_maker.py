import glob
out=''
fqs=glob.glob('../*_1_val_1.fq.gz')
for file in fqs:
	newn=file[0:-14]
	out+=newn+'\n'
with open('slm_list.txt','w') as fh:
	fh.write(out)
