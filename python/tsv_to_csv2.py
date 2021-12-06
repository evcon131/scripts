def tsv_to_csv2(infile, outfile='out.csv2'):
	out=''
	with open(infile) as fh:
		for line in fh:
			if line[0]!='#':
				line=line.replace('\t',';')
				out+=line
	with open(outfile, 'w') as fh:
		fh.write(out)
if __name__ == '__main__':
	import sys
	tsv_to_csv2(sys.argv[1])