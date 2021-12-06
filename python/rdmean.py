def rdmean(infile, outfile):
	from statistics import mean
	out=''
	with open(infile) as fh:
		for line in fh:
				outline=''
				pbleb_mean_ref_reads=[]
				pbleb_mean_alt_reads=[]
				control_mean_ref_reads=[]
				control_mean_alt_reads=[]
				ll=line.split('\t')
				for item in ll[0:18]:
					outline+='\t'+item
				for i in range(18,28,2):
					pbleb_mean_ref_reads.append(float(ll[i]))
				for i in range(19,29,2):
					pbleb_mean_alt_reads.append(float(ll[i]))
				if ll[33]!='':
					for i in range(28,38,2):
						control_mean_ref_reads.append(float(ll[i]))
					for i in range(29,38,2):
						control_mean_alt_reads.append(float(ll[i]))
				else:
					control_mean_ref_reads=[0]
					control_mean_alt_reads=[0]
				outline+='\t'+str(mean(pbleb_mean_ref_reads))
				outline+='\t'+str(mean(pbleb_mean_alt_reads))
				outline+='\t'+str(mean(control_mean_ref_reads))
				outline+='\t'+str(mean(control_mean_alt_reads))
				for item in ll[18:len(ll)]:
					outline+='\t'+item
				out+=outline

	with open(outfile,'w') as fh:
		fh.write(out)

if __name__ == '__main__':
	import sys
	rdmean(sys.argv[1], sys.argv[2])
CI100354





#SYMBOL	GENE_ID	TYPE	EFFECT	CHR	POS	ID	REF	ALT	QUAL	FILTER	INFO	EXTRA_INFO	CI100354.info	CI101227.info	CI104637.info	CI87605.info	CI96367.info	ref_pbleb_reads_mean	alt_pbleb_reads_mean	ref_control_reads_mean	alt_control_reads_mean	CI100354.ref_reads	CI100354.alt_reads	CI101227.ref_reads	CI101227.alt_reads	CI104637.ref_reads	CI104637.alt_reads	CI87605.ref_reads	CI87605.alt_reads       CI96367.ref_reads	CI96367.alt_reads	CIC87067.ref_reads	CIC87067.alt_reads	CIC87190.ref_reads	CIC87190.alt_reads	CIC87791.ref_reads	CIC87791.alt_reads	CIC93524.ref_reads	CIC93524.alt_reads	CIC94767.ref_reads	CIC94767.alt_reads	in722
