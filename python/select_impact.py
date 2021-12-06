def select_impact(infile, outfile):
	out=''
	with open(infile) as fh:
		for line in fh:
			if line[0] != '#':
				if ('missense_variant' or 'frameshift_variant' or 'stop_gained' or 'start_lost') in line:
						if 'missense_variant' in line:
							out+=line
	with open(outfile,'w') as fh:
		fh.write(out)

if __name__ == '__main__':
	import sys
	select_impact(sys.argv[1], sys.argv[2])