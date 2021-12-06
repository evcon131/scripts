def script_maker(prefix):
	import gzip
	import io
	import time
	import sys
	import os
	import glob
	if os.path.exists('trimmed_reads') == False:
		os.mkdir("trimmed_reads")
	if os.path.exists("star") == False:
		os.mkdir("star")
	sys.stdout.write('reading files...\n')
	sys.stdout.flush()
	file_list= sorted(glob.glob(prefix+"*"))
	for i in range(0,len(file_list),2):
		out_script='#!/bin/bash\n'
		out_script+='cd trimmed_reads\n'
		out_script+= ('trim_galore -j 4 --paired --fastqc --path_to_cutadapt /lab_data/avery_lab/apps/bin/cutadapt \\\n../'+file_list[i]+' ../'+file_list[i+1]+'\n\n') 
		file1=file_list[i]
		file2=file_list[i+1]
		if "/" in file1:
			fl=file1.split("/")
			file1=fl[len(fl)-1]
		if "/" in file2:
			fl=file2.split("/")
		file2=fl[len(fl)-1]
		prefix=file1[0:-8]+"_"
		out_file_name=file1[0:-8]+'.sh'
		file1='../trimmed_reads/'+file1[0:-6]+'_val_1.fq.gz'
		file2='../trimmed_reads/'+file2[0:-6]+'_val_2.fq.gz'
		out_script+='cd ../star\n'
		out_script+='STAR \\\n--genomeDir /lab_data/avery_lab/reference_files/cf3_str.20.7.1 \\\n--outSAMtype BAM Unsorted \\\n--genomeLoad LoadAndRemove \\\n--quantMode GeneCounts \\\n--readFilesCommand zcat \\\n--runThreadN 6 \\\n--outFileNamePrefix '+ prefix+' \\\n--readFilesIn '+file1+' '+file2+'\n\n'
		out_script+="samtools sort -o "+prefix+".sorted.bam "+prefix+ "Aligned.out.bam\n\n"
		out_script+="samtools index "+prefix+".sorted.bam\n\n"
		out_script+="bamCoverage -bs 1 -b "+prefix+".sorted.bam -o "+prefix[0:-1]+".bw\n\n" 
		with open(out_file_name,'w') as fh:
			fh.write(out_script)
		os.chmod(out_file_name,0o777)
	sys.stdout.write('Woo! Done!\n')
	sys.stdout.flush()
if __name__ == '__main__':
	import sys
	prfx=sys.argv[1]
	script_maker(prfx)



