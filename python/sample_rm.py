def sample_rm(infile, prefix):
	outfile="out.vcf"
	with open(infile) as fh:
		for line in fh:
			if "#" not in line[0]:
				ll=line.split("\t")
				if prefix not in ll[len(ll)-1]:
					with open(outfile, 'a') as fh:
							fh.write(line)
if __name__ == '__main__':
	import sys
	sample_rm(sys.argv[1], sys.argv[2])