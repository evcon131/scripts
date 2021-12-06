def map_percnt_plt(prefix):
	import glob
	import matplotlib.pyplot as plt
	import numpy as np
	import seaborn as sns
	import pandas as pd
	y=[]
	cf3f=glob.glob(prefix+'/*cf3*')
	cf4f=glob.glob(prefix+'/*cf4*')
	bsf=glob.glob(prefix+'/*bs*')
	gdf=glob.glob(prefix+'/*gd*')
	cf3=[]
	cf4=[]
	basenji=[]
	gd=[]
	for file in cf3f:
		with open(file) as fh:
			for line in fh:
				if "Uniquely mapped reads %" in line:
					line=line.strip()
					item=line.split("\t")[1]
					prcnt=float(item.replace("%",""))
					cf3.append(prcnt)
					y.append(prcnt)
	for file in cf4f:
		with open(file) as fh:
			for line in fh:
				if "Uniquely mapped reads %" in line:
					line=line.strip()
					item=line.split("\t")[1]
					prcnt=float(item.replace("%",""))
					cf4.append(prcnt)
					y.append(prcnt)
	for file in bsf:
		with open(file) as fh:
			for line in fh:
				if "Uniquely mapped reads %" in line:
					line=line.strip()
					item=line.split("\t")[1]
					prcnt=float(item.replace("%",""))
					basenji.append(prcnt)
					y.append(prcnt)
	for file in gdf:
		with open(file) as fh:
			for line in fh:
				if "Uniquely mapped reads %" in line:
					line=line.strip()
					item=line.split("\t")[1]
					prcnt=float(item.replace("%",""))
					gd.append(prcnt)
					y.append(prcnt)

	x=np.concatenate((np.repeat("cf3",14),np.repeat("cf4",14),np.repeat("Basenji",14),np.repeat("Great\nDane",14)))

	pltd=pd.DataFrame({'genome':x, 'prcet':y})
	print(pltd.groupby('genome').mean())
	mns=pltd.groupby('genome').mean()['prcet']

	sns.set_palette("colorblind")
	sns.stripplot(x=x, y=y)
	labels = [e.get_text() for e in plt.gca().get_xticklabels()]
	ticks = plt.gca().get_xticks()
	w = 0.1
	plt.hlines(mns[2], ticks[0]-w, ticks[0]+w, colors=sns.color_palette("colorblind")[0])
	plt.hlines(mns[3], ticks[1]-w, ticks[1]+w, colors=sns.color_palette("colorblind")[1])
	plt.hlines(mns[0], ticks[2]-w, ticks[2]+w, colors=sns.color_palette("colorblind")[2])
	plt.hlines(mns[1], ticks[3]-w, ticks[3]+w, colors=sns.color_palette("colorblind")[3])
	plt.ylabel("Percent Mapped")
	plt.show()
if __name__ == '__main__':
	import sys
	map_percnt_plt(sys.argv[1])



