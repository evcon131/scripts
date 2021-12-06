STAR \
--genomeDir /lab_data/avery_lab/reference_files/cf3_str.19.11.9 \
--outSAMtype BAM SortedByCoordinate \
--twopassMode Basic \
--readFilesCommand zcat \
--runThreadN 6 \
--outFileNamePrefix TZL38094 \
--readFilesIn ../../trim/TZL38094_1_val_1.fq.gz  ../../trim/TZL38094_2_val_2.fq.gz

java -jar /lab_data/avery_lab/apps/gatk-4.1.4.1/gatk-package-4.1.4.1-local.jar SplitNCigarReads \
-I TZL38094Aligned.sortedByCoord.out.bam \
-R /lab_data/avery_lab/reference_files/Canis_familiaris.CanFam3.1.dna.toplevel.fa \
-O output.bam

java -jar /lab_data/avery_lab/apps/java_jars/picard.jar AddOrReplaceReadGroups \
I=output.bam \
O=output_with_RG.bam \
SORT_ORDER=coordinate \
RGID=foo \
RGLB=bar \
RGPU=UNIT1 \
RGPL=illumina \
RGSM=Sample1 \
CREATE_INDEX=True

java -jar /lab_data/avery_lab/apps/gatk-4.1.4.1/gatk-package-4.1.4.1-local.jar BaseRecalibrator \
-I output_with_RG.bam \
--known-sites /lab_data/avery_lab/reference_files/canis_familiaris.vcf \
-R /lab_data/avery_lab/reference_files/Canis_familiaris.CanFam3.1.dna.toplevel.fa \
-O recal.txt

java -jar /lab_data/avery_lab/apps/gatk-4.1.4.1/gatk-package-4.1.4.1-local.jar ApplyBQSR \
-R /lab_data/avery_lab/reference_files/Canis_familiaris.CanFam3.1.dna.toplevel.fa \
-I output_with_RG.bam \
--bqsr-recal-file recal.txt \
-O output_absqr.bam

java -Xmx4g -jar /lab_data/avery_lab/apps/gatk-4.1.4.1/gatk-package-4.1.4.1-local.jar HaplotypeCaller \
-R /lab_data/avery_lab/reference_files/Canis_familiaris.CanFam3.1.dna.toplevel.fa \
-I output_absqr.bam \
-O TZL38094.vcf.gz

java -Xmx1g -jar /lab_data/avery_lab/apps/snpEff/snpEff.jar \
-v CanFam3.1.86 \
-stats stats.html \
t_filter.720sub.csub.selectann.af_rd.vcf > sub_ann.vcf

python3 snp_filter.py #merge all t files, must be protein coding add ID
python3 snp_subtractor.py #sub 720g 
python3 snp_control_subtractor.py 
python3 snp_subtractor.py #sub ensembl
python3 snp_af_rd_filter.py #filter allele frequency read depth
python3 select_annotation.py #select nonsynonomous snps
python3 hit_counter.py #make hit list
python3 hitlist_bysample_df_converter.py

t_filter.720sub.csub.vcf
t_filter.720sub.csub.selrctann.vcf
t_filter.720sub.csub.selectann.af_rd.vcf

