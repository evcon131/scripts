def gene_read_extractor(infile, chrm, start, stop, outname):
	import os
	outs='#!/bin/bash\n'
	infile_pos_srt=infile[0:-4]+'.psrt.bam'
	range_bam=outname+'.bam'
	range_bam_srt=outname+'.srt.bam'
	outs+='echo "starting sort..."\n'
	outs+='samtools sort -o '+infile_pos_srt+' '+infile+'\n'
	outs+='echo "finished initial sort, starting index"\n'
	outs+='samtools index '+infile_pos_srt+'\n'
	outs+='echo "finished index, starting read extraction"\n'
	outs+='samtools view -h '+infile_pos_srt
	outs+=' '+chrm+':'+start+'-'+stop+' > '
	outs+=range_bam+'\n'
	outs+='samtools sort -n -o '+range_bam_srt+' '+range_bam+'\n'
	outs+='samtools fastq -1 '+outname+'_1.fq -2 '+outname+'_2.fq '+range_bam_srt
	with open(outname+'.sh', 'w') as fh:
		fh.write(outs)
		os.chmod(outname+'.sh',0o777)
if __name__ == '__main__':
	import sys
	if len(sys.argv)!=6:
		print('USAGE:\n')
		print('python3 /lab_data/avery_lab/example_comands/python_scripts/gene_read_extractor.py <in_bam> <chromosome> <start> <stop> <out_filename>\n')
		print('EXAMPLE:\ngene:ThPOK')
		print('in bam: TZL36988.bam')
		print('chromosome: 7')
		print('start: 42468247')
		print('stop: 42483436')
		print('out file: TZL36988thpok\n')
		print('python3 /lab_data/avery_lab/example_comands/python_scripts/gene_read_extractor.py TZL36988.bam 7 42468247 42483436 TZL36988thpok')

	else:
		gene_read_extractor(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])