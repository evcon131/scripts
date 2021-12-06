def scat_ploter(infile):
	from matplotlib import pyplot as plt
	import seaborn as sns
	import pandas as pd
	import numpy as np
	f, axes = plt.subplots(2, 3)
	y_all=[]
	with open(infile) as fh:
		line=fh.readline()
		ll=line.split(",")
		cd8_samples = ll[1:4]
		cd4_samples = ll[4:8]
		tzn_samples = ll[8:13]
		for i in range(len(tzn_samples)):
			tzn_samples[i] = tzn_samples[i].replace("tzn_", "")
		for i in range(len(cd8_samples)):
			cd8_samples[i] = cd8_samples[i].replace("CD8_", "")
		for i in range(len(cd4_samples)):
			cd4_samples[i] = cd4_samples[i].replace("CD4_", "")
		for line in fh:
			ll=line.split(",")
			for item in ll[1:13]:
				y_all.append(float(item))



	x=["CD8","CD8","CD8","CD4","CD4","CD4","CD4","T Zone","T Zone","T Zone","T Zone","T Zone"]			
	THPOK = y_all[0:12]
	BCL6=y_all[12:24]
	TBX21=y_all[24:36]
	FOXP3=y_all[36:48]
	RORC=y_all[48:60]
	GATA3=y_all[60:72]

	sns.stripplot(x=x, y=THPOK,  ax=axes[0, 0]).set(title='THPOK')
	sns.stripplot(x=x, y=BCL6,  ax=axes[0, 1]).set(title='BCL6')
	sns.stripplot(x=x, y=TBX21,  ax=axes[0, 2]).set(title='TBX21')
	sns.stripplot(x=x, y=FOXP3,  ax=axes[1, 0]).set(title='FOXP3')
	sns.stripplot(x=x, y=RORC,  ax=axes[1, 1]).set(title='ROR'+r'$\gamma$'+'T')
	sns.stripplot(x=x, y=GATA3,  ax=axes[1, 2]).set(title='GATA3')
	sns.stripplot(x=x, y=EOMES,  ax=axes[2, 0]).set(title='EOMES')

	# ax.annotate("",
 #            xy=(2, sat_mean), xycoords='data',
 #            xytext=(.5, .5), textcoords='axes fraction',
 #            horizontalalignment="center",
 #            arrowprops=dict(arrowstyle="->",
 #                            connectionstyle="arc3"),
 #            bbox=dict(boxstyle="round", fc="w"),
 #            )
#ax.get_figure().savefig('tips_annotation.png')


	# distance across the "X" or "Y" stipplot column to span, in this case 40%
	mean_width = 0.4

	#for tick, text in zip(axes[0, 0].get_xticks(), axes[0, 0].get_xticklabels()):
	#	sample_name = text.get_text("X")  # "X" or "Y"

		# calculate the mean value for all replicates of either X or Y
	#means = [np.mean(THPOK[0:3]),np.mean(THPOK[3:8]),np.mean(THPOK[8:15])]
		# plot horizontal lines across the column, centered on the tick
	#axes[0, 0].plot([tick-mean_width/2, tick+mean_width/2], means,lw=4, color='k')
	plt.subplots_adjust(wspace=.4,hspace=.4)

	f.set_figwidth(9)
	#plt.show()
	plt.savefig("fig1.pdf")
if __name__ == '__main__':
	import sys
	scat_ploter(sys.argv[1])





