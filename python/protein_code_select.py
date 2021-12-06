def protein_code(infile, outfile):
	out=''
	with open(infile) as fh:
		for line in fh:
			if line[0] != '#':
				if 'protein_coding' in line:
						if 'missense_variant' in line:
							out+=line
	with open(outfile,'w') as fh:
		fh.write(out)

if __name__ == '__main__':
	import sys
	protein_code(sys.argv[1], sys.argv[2])