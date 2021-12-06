import gzip
import io
import time
import sys
import os
import glob
sys.stdout.write('reading files...\n')
sys.stdout.flush()
file_list=sorted(glob.glob('*.gz'))
for i in range(0,len(file_list),2):
	out_script='#!/bin/bash\n'
	if '_val_' not in file_list[i]:
		sys.stdout.write(file_list[i]+' and '+file_list[i+1]+' will be trimmed\n')
		sys.stdout.flush()
		out_script+= ('trim_galore -j 4 --paired --fastqc --path_to_cutadapt /lab_data/avery_lab/apps/bin/cutadapt \\\n'+file_list[i]+' '+file_list[i+1]+'\n\n') 
	if '_val_' not in file_list[i]:
		file1=file_list[i][0:-6]+'_val_1.fq.gz'
		file2=file_list[i+1][0:-6]+'_val_2.fq.gz'
	else:
		file1=file_list[i]
		file2=file_list[i+1]
	out_script+='mkdir '+file1[0:-14]+'\n'
	out_script+='cd '+file1[0:-14]+'\n'
	out_script+='STAR \\\n--genomeDir /lab_data/avery_lab/reference_files/cf3_str.20.7.1 \\\n--outSAMtype BAM SortedByCoordinate \\\n--twopassMode Basic \\\n--readFilesCommand zcat \\\n--runThreadN 6 \\\n--outFileNamePrefix '+ file1[0:-14]+'_ \\\n--readFilesIn ../'+file1+' ../'+file2+'\n\n'
	out_script+='java -jar /lab_data/avery_lab/apps/gatk-4.1.4.1/gatk-package-4.1.4.1-local.jar SplitNCigarReads \\\n'
	out_script+='-I '+file1[0:-14]+'Aligned.sortedByCoord.out.bam \\\n-R /lab_data/avery_lab/reference_files/Canis_familiaris.CanFam3.1.dna.toplevel.fa \\\n-O output.bam\n\n'
	out_script+='java -jar /lab_data/avery_lab/apps/java_jars/picard.jar AddOrReplaceReadGroups \\\nI=output.bam \\\nO=output_with_RG.bam \\\nSORT_ORDER=coordinate \\\nRGID=foo \\\nRGLB=bar \\\nRGPU=UNIT1 \\\nRGPL=illumina \\\nRGSM=Sample1 \\\nCREATE_INDEX=True\n\n'
	out_script+='java -jar /lab_data/avery_lab/apps/gatk-4.1.4.1/gatk-package-4.1.4.1-local.jar BaseRecalibrator \\\n-I output_with_RG.bam \\\n--known-sites /lab_data/avery_lab/reference_files/canis_familiaris.vcf \\\n-R /lab_data/avery_lab/reference_files/Canis_familiaris.CanFam3.1.dna.toplevel.fa \\\n-O recal.txt\n\n'
	out_script+='java -jar /lab_data/avery_lab/apps/gatk-4.1.4.1/gatk-package-4.1.4.1-local.jar ApplyBQSR \\\n-R /lab_data/avery_lab/reference_files/Canis_familiaris.CanFam3.1.dna.toplevel.fa \\\n-I output_with_RG.bam \\\n--bqsr-recal-file recal.txt \\\n-O output_absqr.bam\n\n'
	out_script+='java -Xmx40g -jar /lab_data/avery_lab/apps/gatk-4.1.4.1/gatk-package-4.1.4.1-local.jar HaplotypeCaller \\\n-R /lab_data/avery_lab/reference_files/Canis_familiaris.CanFam3.1.dna.toplevel.fa \\\n-I output_absqr.bam \\\n-O '+file1[0:-14]+'.vcf.gz\n\n'
	out_script+='java -Xmx10g -jar /lab_data/avery_lab/apps/snpEff/snpEff.jar \\\n-v CanFam3.1.100 \\\n-stats stats.html \\\n'
	out_script+=file1[0:-14]+'.vcf.gz > '+file1[0:-14]+'_ann.vcf\n\n'
	out_script+='python3 /lab_data/avery_lab/example_comands/python_scripts/vcf_dir_maker.py\n\n'
	vcf=file1[0:-14]+'_ann.vcf'
	out_script+='mv '+vcf+' ../all_VCF/\n\n'
	out_file_name=file1[0:-14]+'.sh'
	with open(out_file_name,'w') as fh:
		fh.write(out_script)
	os.chmod(out_file_name,0o777)
if not os.path.exists('all_VCF'):
	os.mkdir('all_VCF')
sys.stdout.write('Woo! Done!\n')
sys.stdout.flush()


