def gsea_adj(infile):
	import numpy as np
	from matplotlib import pyplot as plt
	refd={}
	with open(infile) as fh:
		for line in fh:
			inline_allready=[]
			ll=line.split(",")
			new_ll=ll[0].split("_")
			for item in new_ll:
				if "GSE" not in item:
					if "UP" not in item:
						if "DN" not in item:
							if "VS" not in item:
								if item not in inline_allready:
									if item not in refd:
										refd[item]=1
										inline_allready.append(item)
									else:
										refd[item]+=1
										inline_allready.append(item)
	X=[]
	Y=[]
	label=[]
	real_eff=0
	for key in refd:
		if (key == "EFF") or (key == "EFFECTOR"):
			real_eff+=refd[key]
	refd["EFFECTOR"]=real_eff
	for key in refd:
		#print(key+" "+str(refd[key]))
		if int(refd[key]) >= 20:
			X.append(key)
			Y.append(int(refd[key]))
			if "CD" in key:
				label.append(key)
			else:
				label.append(key.title())
	fig, ax = plt.subplots()
	ax.bar(np.arange(len(X)), Y)
	ax.set_xticks(np.arange(len(X)))
	ax.set_xticklabels(label)
	ax.set_ylabel('Number Enriched Genesets Containing')
	ax.set_title('Most Common Geneset Adjectives')
	ax.set_xlabel('Geneset Descriptor')

#	plt.show()
	plt.savefig("gsea terms bar.pdf")

if __name__ == '__main__':
	import sys
	gsea_adj(sys.argv[1])





