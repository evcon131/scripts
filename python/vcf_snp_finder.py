import gzip
import io
import time
import sys
import os
import glob
with open(sys.argv[1]) as fh:
	for line in fh:
		if '#' not in line[0]:
			ll=line.split('\t')
			sample_id=ll[len(ll)-1]
			sample_id=sample_id.strip()
			chromosome=ll[0]
			pos=ll[1]
			ref=ll[3]
			alt=ll[4]
			ll=ll[7].split('|')	
			gene=ll[3]
			sub=ll[10]
			sub=sub.replace('p.','')
			if pos == str(sys.argv[2]):
				if ref == sys.argv[3]:
					if alt == sys.argv[4]:
						print(line)


