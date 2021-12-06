def gtf_converter(infile, outfile="out.gtf"):
	out=""
	with open(infile) as fh:
		for line in fh:
			if "#" not in line[0]:
				ll=line.split("\t")
				if "chr" in ll[0]:
					line=line.replace("chr","")
					out+=line
					typ="UCSC"
				else:
					line="chr"+line
					out+=line
					typ="Ensemnl"
			else:
				out+=line

	if typ=="UCSC":
		print("UCSC type detected, converted to ensembk")
	else:
		print("Ensemnl type detected, converted to UCSC")
	with open(outfile, "w") as fh:
		fh.write(out)

if __name__=="__main__":
	import sys
	gtf_converter(sys.argv[1])

