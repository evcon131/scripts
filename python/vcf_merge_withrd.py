def merge_vcf_dict(prefix, outf='out.vcf'):
	import glob
	import time
	merge_dict={}
	merge_list=[]
	file_list=glob.glob(prefix+'*')
	len_ad=2
	out=''
	with open(file_list[0]) as fh:
		for line in fh:
			line=line.strip()
			ll = line.split('\t')
			chromosome=ll[0].replace('chr','')
			pos=ll[1]
			huh=ll[2]
			ref=ll[3]
			alt=ll[4]
			variant=chromosome+';'+pos+';'+huh+';'+ref+';'+alt
			if variant in merge_dict:
				merge_dict[variant].append(ll[10])
				merge_dict[variant].append(ll[11])
			else:#variant not in merge_dict:
				merge_dict[variant]=[ll[10]]
				merge_dict[variant].append(ll[11])
	for file in file_list[1:len(file_list)]:	
		starttime=time.time()
		print(file)
		len_ad+=2
		print(len_ad)
		with open(file) as fh:
			for line in fh:
				line=line.strip()
				ll = line.split('\t')
				chromosome=ll[0].replace('chr','')
				pos=ll[1]
				huh=ll[2]
				ref=ll[3]
				alt=ll[4]
				variant=chromosome+';'+pos+';'+huh+';'+ref+';'+alt
				if variant in merge_dict:
					merge_dict[variant].append(ll[10])
					merge_dict[variant].append(ll[11])
				else:#variant not in merge_dict:
					merge_dict[variant]=[ll[10]]
					merge_dict[variant].append(ll[11])					
			for key in merge_dict:
				if len(merge_dict[key]) == 2:
					for _ in range(2, len_ad):
						merge_dict[key].insert(0,'0')
			for key in merge_dict:
				if len(merge_dict[key]) < len_ad:
					merge_dict[key].append('0')
					merge_dict[key].append('0')

		newtime=time.time()
		timeelapsed = newtime-starttime
		minutes = timeelapsed / 60
		hours = minutes / 60
		displayminutes=format(minutes, '.2f') 
		displayhours=format(hours, '.2f') 
		if minutes < 60:
			sys.stdout.write('time to analyse file '+str(displayminutes)+' minutes\n')
			sys.stdout.flush()
		else:
			sys.stdout.write('time to analyse file '+str(displayhours)+' hours\n')
			sys.stdout.flush()

	for key in merge_dict:
		outl=key
		outl+=';'+';'+';'+';'+';'
		for item in merge_dict[key]:
			outl+=';'+str(item)		
		outl+='\n'
		out+=outl
	with open(outf, 'w') as fh:
		fh.write(out)

if __name__ == '__main__':
	import sys
	merge_vcf_dict(sys.argv[1])	


