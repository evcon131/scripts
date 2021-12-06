def genome_snpeff_finder(file):
	with open(file) as fh:
		for line in fh:
			if "CanFam" in line:
				print(line)
if __name__ == '__main__':
	import sys
	genome_snpeff_finder(sys.argv[1])


java -jar snpEff.jar build -gtf22 -v CanFam3.1.100