def biotype_finder(infile):
	btypel=[]
	with open(infile) as fh:
		for line in fh:
			if line[0]!="#":
				line=line.strip()
				ll=line.split("\t")
				ll=ll[8].split(";")
				for item in ll:
					if "gene_biotype" in item:
						item=item.replace(" transcript_biotype ","")
						if item not in btypel:
							btypel.append(item)
	for item in btypel:
		print(item)
if __name__ == '__main__':
	import sys
	biotype_finder(sys.argv[1])

