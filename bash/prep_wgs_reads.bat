trim_galore -j 4 --paired --fastqc \
--path_to_cutadapt /lab_data/avery_lab/apps/bin/cutadapt \
CIC94767_CSFP200006408-1a_HJVFHDSXY_L2_1_val_1.fq.gz \ \
CIC94767_CSFP200006408-1a_HJVFHDSXY_L2_1_val_1.fq.gz \

/bwa mem -t 6 \
lab_data/avery_lab/reference_files/bwa_ref/canfam3 \
../trim/CIC94767_CSFP200006408-1a_HJVFHDSXY_L2_1_val_1.fq.gz \
../trim/CIC94767_CSFP200006408-1a_HJVFHDSXY_L2_2_val_2.fq.gz \
| samtools view -b -@ 6 - | samtools sort -@ 6 - > CIC94767.bam 


gatk MarkDuplicates \
-I CIC94767_CSFP200006408-1a_HJVFHDSXY_L2.bam \
-O CIC94767.markdup.bam \
--METRICS_FILE sure13


samtools sort -@ 6 CIC94767.markdup.bam > CIC94767.markdup.srt.bam

gatk AddOrReplaceReadGroups \
-I CIC94767.markdup.bam \
-O CIC94767.RG.bam \
-SORT_ORDER coordinate \
-RGID CIC94767 \
-RGLB CIC94767 \
-RGPU UNIT1 \
-RGPL illumina \
-RGSM CIC94767 \
-CREATE_INDEX True


gatk BaseRecalibrator \
-I CIC94767.RG.bam \
-R /lab_data/avery_lab/reference_files/Canis_familiaris.CanFam3.1.dna.toplevel.fa \
--known-sites /lab_data/avery_lab/reference_files/canis_familiaris.vcf \ #Ensembl
-O CIC94767.recal_data.table

gatk ApplyBQSR \
-R /lab_data/avery_lab/reference_files/Canis_familiaris.CanFam3.1.dna.toplevel.fa-I CIC94767.RG.bam \
--bqsr-recal-file CIC94767.recal_data.table \
-O CIC94767.bqsr.bam

gatk --java-options "-Xmx4g" HaplotypeCaller \
-R /lab_data/avery_lab/reference_files/Canis_familiaris.CanFam3.1.dna.toplevel.fa \
-I CIC94767.RG.bam \
-O CIC94767.g.vcf.gz \
-ERC GVCF

gatk --java-options "-Xmx4g -Xms4g" GenomicsDBImport \
-V CI100354.g.vcf.gz \
-V CI101227.g.vcf.gz \
-V CI104637.g.vcf.gz \
-V CI87605.g.vcf.gz \
-V CI96367.g.vcf.gz \
--genomicsdb-workspace-path pbleb_X \
-L X
ref_reads.CI100354	alt_reads.CI100354	

gatk --java-options "-Xmx4g" GenotypeGVCFs \
-R /lab_data/avery_lab/reference_files/Canis_familiaris.CanFam3.1.dna.toplevel.fa \
-V gendb://pbleb_X \
-O pbleb_X.vcf.gz

julia /lab_data/avery_lab/example_comands/julia_language/vcf_subtractor.jl \
pblebs.vcf \
/lab_data/avery_lab/reference_files/722g.990.SNP.INDEL.chrAll.vcf.eidx \
out.vcf

java -Xmx10g -jar ~/apps/snpEff/snpEff.jar ann \
-stats stats.html \
canfam3.1.103 \
pbleb_X.vcf > out.vcf

#!/bin/bash
#SBATCH --partition=shas
#SBATCH --qos normal 
#SBATCH -t 20:00:00
#SBATCH -N 1
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=END
#SBATCH --mail-user=evan.conaway@gmail.com 
#SBATCH -c 6 
/projects/evcon\@colostate.edu/bwa/bwa mem -t 6 \
../bwa_ref/canfam3 \
../trim/CIC94767_CSFP200006408-1a_HJVFHDSXY_L2_1_val_1.fq.gz \
../trim/CIC94767_CSFP200006408-1a_HJVFHDSXY_L2_2_val_2.fq.gz \
| samtools view -b -@ 6 - | samtools sort -@ 6 - > CIC94767.bam 

java -Xmx10g -jar ~/snpEff/snpEff.jar ann \
-stats stats.html \
CanFam3.1.99 \
pblebs.vcf > pblebs.ann.vcf

#! /bin/bash
#SBATCH --partition=shas
#SBATCH --qos=normal
#SBATCH -t 3:00:00
#SBATCH -N 1
#SBATCH --mail-type=END
#SBATCH --mail-user=evan.conaway@gmail.com
#SBATCH --array=0-9
#SBATCH --mem=40000

ml jdk

names=($(cat sids.txt))


/projects/evcon\@colostate.edu/gatk-4.2.0.0/gatk --java-options "-Xmx4g" HaplotypeCaller \
-R /projects/evcon\@colostate.edu/ref/Canis_familiaris.CanFam3.1.dna.toplevel.fa
-I ${names[${SLURM_ARRAY_TASK_ID}]}.RG.bam \
-O ${names[${SLURM_ARRAY_TASK_ID}]}.vcf \
-ERC GVCF

/projects/evcon\@colostate.edu/gatk-4.2.0.0/gatk BaseRecalibrator \
-I ${names[${SLURM_ARRAY_TASK_ID}]}.RG.bam \
-R /lab_data/avery_lab/reference_files/Canis_familiaris.CanFam3.1.dna.toplevel.fa \
--known-sites /lab_data/avery_lab/reference_files/canis_familiaris.vcf \ #Ensembl
-O ${names[${SLURM_ARRAY_TASK_ID}]}.recal_data.table

/projects/evcon\@colostate.edu/gatk-4.2.0.0/gatk BaseRecalibrator \
-I ${names[${SLURM_ARRAY_TASK_ID}]}.RG.bam \
-R /projects/evcon\@colostate.edu/ref/Canis_familiaris.CanFam3.1.dna.toplevel.fa \
--known-sites /projects/evcon\@colostate.edu/ref/canis_lupus_familiaris.vcf \
-O ${names[${SLURM_ARRAY_TASK_ID}]}.recal_data.table \
--tmp-dir tmp

/projects/evcon\@colostate.edu/gatk-4.2.0.0/gatk ApplyBQSR \
-R /projects/evcon\@colostate.edu/ref/Canis_familiaris.CanFam3.1.dna.toplevel.fa \
--bqsr-recal-file ${names[${SLURM_ARRAY_TASK_ID}]}.recal_data.table \
-O ${names[${SLURM_ARRAY_TASK_ID}]}.bqsr.bam \
--tmp-dir tmp

ref_reads.CIC87067	alt_reads.CIC87067	ref_reads.CIC87190	alt_reads.CIC87190	ref_reads.CIC87791	alt_reads.CIC87791	ref_reads.CIC93524	alt_reads.CIC93524	ref_reads.CIC94767	alt_reads.CIC94767