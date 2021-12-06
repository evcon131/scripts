def jxn_file(infile):
	out=""
	with open(infile) as fh:
		fh.readline()
		for line in fh:
			ll=line.split("\t")
			if len(ll) > 7:
				bpl1=ll[8]
				bpl2=ll[9]
				bpl1=bpl1.split(":")
				bpl2=bpl2.split(":")
				chr1="cf"+bpl1[0]
				chr2="cf"+bpl2[0]
				breakpoint1=bpl1[1]
				breakpoint2=bpl2[1]
				out+=chr1+' '+breakpoint1+" "+breakpoint1+' '+chr2+' '+breakpoint2+' '+breakpoint2+'\n'
	with open("out.txt","w") as fh:
		fh.write(out)
if __name__ == '__main__':
	import sys
	jxn_file(sys.argv[1])