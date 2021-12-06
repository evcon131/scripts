def lineCounter(file):
	import gzip
	import io
	cnt=0
	if '.gz' in file:
		with io.TextIOWrapper(io.BufferedReader(gzip.open(file))) as fh:
			for line in fh:
				if '#' not in line:
					cnt+=1
	else:
		with open(file) as fh:
			for line in fh:
				if '#' not in line:
					cnt+=1
	print(str(cnt)+' lines')
if __name__ == '__main__':
	file = input('What file? ')
	import os
	import sys
	file=file.strip()
	if os.path.exists(file) == False:
		print('barnacles! File not found, try again')
		sys.exit()
	lineCounter(file)

