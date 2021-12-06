hdr=''
with open('allc.vcf') as fh:
	for line in fh:
		if '#' in line:
			hdr+=line
with open('t_filter.vcf') as fh:
	opt=hdr
	for line in fh:
		opt+=line
with open('subwhdr.vcf','w') as fh:
	fh.write(opt)
