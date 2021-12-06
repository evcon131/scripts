def csv2_len_fix(infile, outfile='out.vcf'):
	out=''
	with open(infile) as fh:
		for line in fh:
			ll=line.split(';')
			if len(ll) == 21:
				del ll[-11]
			if len(ll) == 31:
				del ll[-11]
			for item in ll:
				out+=';'+item
	with open(outfile, 'w') as fh:
		fh.write(out)
if __name__ == '__main__':
	import sys
	csv2_len_fix(sys.argv[1])