def barplot_from_multiplr_vcfs_vartypes():
	import gzip
	import io
	import time
	import sys
	import os
	import glob
	import mygene
	import matplotlib.pyplot as plt; plt.rcdefaults()
	import numpy as np
	import matplotlib.pyplot as plt
	from pylab import rcParams
	fig, ax = plt.subplots()
	rcParams['figure.figsize'] = 100, 100
	var_type=[]
	var_nums=[]
	badfiles=[]
	llll=[]
	mg = mygene.MyGeneInfo()
	out="variant_type, file, number\n"
	dlist=[]
	outd={}
	file_list=glob.glob("t_*")
	for file in file_list:
		with open(file) as fh:
			sys.stdout.write(file+'\n')
			sys.stdout.flush()			
			for line in fh:
				if '#' not in line[0]:
					ll=line.split('\t')
					ll=ll[7].split('|')	
					for i in range(1,len(ll)-6,15):
						variant_type=ll[i]
						if variant_type not in outd:
							outd[variant_type]={file:1}
						else:
							if file not in outd[variant_type]:
								outd[variant_type][file]=1
							elif file in outd[variant_type]:
								outd[variant_type][file]+=1	
	#for key in refd:
	#	print(key)
	#	print(str(refd[key]))
	for key in outd:
			out+=key
			for filename in outd[key]:
				if filename =="t_filter.rdf.csub.selectann.vcf":
					print(key)
				out+=','+filename
				out+=','+str(outd[key][filename])+"\n"
	with open('variant_type.csv','w') as fh:
		fh.write(out)


	# plotdict={}
	# for tempd in dlist:
	# 	for key in tempd:
	# 		if key not in plotdict:
	# 			plotdict[key]=[]
	# for i in range(len(dlist)):
	# 	for key in dlist[i]:
	# 		out+=key+","+str(tempd[key])+","+file_list[i]+"\n"
	# for key in plotdict:
	# 	var_type.append(key)
	# 	for tempd in dlist:
	# 		if key not in tempd:
	# 			plotdict[key].append(0)
	# 		else:
	# 			plotdict[key].append(int(tempd[key]))
	# valuelist=[]
	# group_labels=[]
	# width = 0.1
	# fig, ax = plt.subplots()
	# for file in file_list:
	# 	name=file+"list"
	# 	valuelist.append(name)
	# 	group_labels.append(file)
	# rectlist=[]
	# odds=[]
	# widthchangelist=[]
	# if len(group_labels) % 2 ==0:
	# 	for i in range(1,len(group_labels)):
	# 		if i%2!=0:
	# 			odds.append(i)
	# 	odds.reverse()
	# 	midpoint=len(group_labels)/2
	# 	for i in range(len(group_labels)):
	# 		widthchangelist.append(width / (len(group_labels) * 2))
	# 	for i in range(len(widthchangelist)/2):
	# 		widthchangelist[i]=widthchangelist[i]*-1*odds[i]
	# 	odds.reverse()
	# 	for i in range(midpoint, len(widthchangelist)):
	# 		widthchangelist[i]=widthchangelist[i]*odds[i]
	# else:
	# 	midpoint=len(group_labels)/2
	# 	for i in range(len(group_labels)):
	# 		widthchangelist.append(width / (len(group_labels)))
	# 	multiplylist=[]
	# 	for i in range(int(midpoint+.5)):
	# 		multiplylist.append(-1*i)
	# 	multiplylist.reverse()
	# 	newwmultiplylist=multiplylist
	# 	multiplylist.reverse()
	# 	for item in multiplylist[1:]:
	# 		newwmultiplylist.append(item)
	# 	for i in range(len(widthchangelist)):
	# 		widthchangelist[i]=widthchangelist[i]+newwmultiplylist[i]
	# labels = var_type
	# y = np.arange(len(labels))  # the label locations
	# width = 5  # the width of the bars
	# for i in range(len(valuelist)):
	# 	plotvalues=[]
	# 	for key in plotdict:
	# 		plotvalues.append(plotdict[key][i])
	# 	holder=ax.barh(y + widthchangelist[i], plotvalues , width, label=valuelist[i])
	# 	rectlist.append(holder)
	


	# # Add some text for labels, title and custom x-axis tick labels, etc.
	# ax.set_ylabel('variant type')
	# ax.set_title('Scores by group and gender')
	# ax.set_yticks(y)
	# ax.set_yticklabels(labels)
	# ax.legend()

	# def autolabel(rects):
	# 	for rect in rects:
	# 		height = rect.get_height()
	# 		ax.annotate('{}'.format(height),
	# 					xy=(rect.get_x() + rect.get_width() / 2, height),
	# 					xytext=(0, 3),  # 3 points vertical offset
	# 					textcoords="offset points",
	# 					ha='center', va='bottom')


	# for col in rectlist:
	# 	autolabel(col)


	# #plt.show()

if __name__ == '__main__':
	barplot_from_multiplr_vcfs_vartypes()


