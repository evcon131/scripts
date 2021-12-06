def novogene_subtractor(prefix):	
	import sys
	import os
	import glob
	filelist=glob.glob(prefix+"*")
	for file in filelist:
		if "/" in file:
			fll=file.split("/")
			file_name=fll[len(fll)-1]
			out_file_name=file_name[0:-15]+".sh"
		else:
			out_file_name=file[0:-15]+".sh"
		out = "#!/bin/bash\njulia /lab_data/avery_lab/example_comands/julia_language/vcf_subtractor.jl "
		out+=file
		out+=" /lab_data/avery_lab/reference_files/722g.990.SNP.INDEL.chrAll.vcf.idx "
		out+=out_file_name[0:-3]
		out+=".720ub.vcf\n"
		with open(out_file_name,'w') as fh:
			fh.write(out)
			os.chmod(out_file_name,0o777)
if __name__ == '__main__':
	import sys
	novogene_subtractor(sys.argv[1])
