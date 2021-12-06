import gzip
import io
import time
import sys
import os
import glob
sys.stdout.write('reading files...\n')
sys.stdout.flush()
file_list=sorted(glob.glob('*.fastq'))
for i in range(0,len(file_list),2):
	out_script='#!/bin/bash\n'
	if '_val_' not in file_list[i]:
		sys.stdout.write(file_list[i]+' and '+file_list[i+1]+' will be trimmed\n')
		sys.stdout.flush()
		out_script+= ('trim_galore -j 4 --paired --fastqc --path_to_cutadapt /lab_data/avery_lab/apps/bin/cutadapt \\\n'+file_list[i]+' '+file_list[i+1]+'\n\n') 
	if '_val_' not in file_list[i]:
		file1=file_list[i][0:-6]+'_val_1.fq'
		file2=file_list[i+1][0:-6]+'_val_2.fq'
	else:
		file1=file_list[i]
		file2=file_list[i+1]
	out_script+='mkdir '+file1[0:-11]+'\n'
	out_script+='cd '+file1[0:-11]+'\n'
	out_script+='STAR \\\n--genomeDir /lab_data/avery_lab/reference_files/human/hg38 \\\n--outSAMtype BAM SortedByCoordinate \\\n--outFilterMultimapNmax 1 \\\n--quantMode GeneCounts \\\n--genomeLoad LoadAndRemove \\\n--limitBAMsortRAM 40000000000 \\\n--runThreadN 6 \\\n--outFileNamePrefix '+ file1[0:-11]+' \\\n--readFilesIn ../'+file1+' ../'+file2+'\n\n'
	out_file_name=file1[0:-11]+'.sh'
	with open(out_file_name,'w') as fh:
		fh.write(out_script)
	os.chmod(out_file_name,0o777)
sys.stdout.write('Woo! Done!\n')
sys.stdout.flush()

