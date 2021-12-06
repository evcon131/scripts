def csv2_to_tsv(infile):
	out=''
	with open(infile) as fh:
		for line in fh:
			line=line.replace(';','\t')
			out+=line
	with open('out.tsv','w') as fh:
		fh.write(out)
if __name__ == '__main__':
	import sys
	csv2_to_tsv(sys.argv[1])