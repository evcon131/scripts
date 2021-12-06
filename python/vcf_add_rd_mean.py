def add_rd_mean(infile, outfile='out.vcf'):
	from statistics import mean
	out=''
	with open(infile) as fh:
		for line in fh:
			if line[0]!='#':
				line=line.strip()
				ll=line.split(';')
				rd_altl=[]
				rd_wtl=[]
				rd_caltl=[]
				rd_cwtl=[]
				af_pblebl=[]
				af_cntrll=[]
				for i in range(11,20,2):
					rd_wtl.append(float(ll[i]))
				for i in range(12,21,2):
					rd_altl.append(float(ll[i]))
				if len(ll) > 25:
					for i in range(21,30,2):
						rd_cwtl.append(float(ll[i]))
					for i in range(22,31,2):
						rd_caltl.append(float(ll[i]))
				for i in range(0,5):
					if (rd_altl[i]!=0) or (rd_wtl[i]!=0):
						af_pblebl.append(rd_altl[i]/(rd_wtl[i]+rd_altl[i]))
					if len(ll) > 25:
						if (rd_caltl[i]!=0) or (rd_cwtl[i]!=0):
							af_cntrll.append(rd_caltl[i]/(rd_caltl[i]+rd_cwtl[i]))
				out+=line
				out+=';'+str(mean(af_pblebl))
				if len(ll) > 25:
					out+=';'+str(mean(af_cntrll))
				out+='\n'

	with open(outfile,'w') as fh:
		fh.write(out)
if __name__ == '__main__':
	import sys
	add_rd_mean(sys.argv[1])

