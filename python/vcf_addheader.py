def vcf_header_add(file1, file2, outfile):
	out=''
	with open(file2) as fh:
		for line in fh:
			if "##" in line[0:3]:
				out+=line
	with open(file1) as fh:
		for line in fh:
			out+=line
	with open(outfile, "w") as fh:
		fh.write(out)

if __name__ == '__main__':
	import sys
	vcf_header_add(sys.argv[1], sys.argv[2], sys.argv[3])

