def vcf_reformat(invcf, outfile='out.vcf'):
	out=''
	with open(invcf) as fh:
		for line in fh:
			if line[0]!='#':
				if len(line) > 6:
					ll=line.split('\t')
					lll=ll[7].split('|')
					for i in range(0,len(lll)-8,15):
						if 'upstream_gene_variant' not in lll[i+1]:
							if 'intron_variant' not in lll[i+1]:
								if 'intergenic_region' not in lll[i+1]:
									if 'downstream_gene_variant' not in lll[i+1]:
										if 'non_coding_transcript' not in lll[i+1]:
											if 'synonymous_variant' not in lll[i+1]:
												kind=lll[i+1]
												geneid=lll[i+4]
												symbol=lll[i+3]
												if lll[i+10]=='':
													eff=lll[i+9]
												else:
													eff=lll[10]
												out+=symbol+'\t'+geneid+'\t'+kind+'\t'+eff
												out+='\t'+line


	with open(outfile,'w') as fh:
		fh.write(out)

if __name__ == '__main__':
	import sys
	if len(sys.argv) > 2:
		vcf_reformat(sys.argv[1], sys.argv[2])
	else:
		vcf_reformat(sys.argv[1])
