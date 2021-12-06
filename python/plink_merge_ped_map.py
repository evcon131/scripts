def plink_merge(prefix):
		import glob
		import pandas as pd
		import sys
		file_list=sorted(glob.glob(prefix+'*'))
		id_list=[]
		pt_list=[]
		out_d={}
		pedlist=[]
		sys.stdout.write('Starting file 1\n')
		sys.stdout.flush()
		with open(file_list[0]) as fh:
			for line in fh:
				idn=line
				id_list.append(idn)
	with open(file_list[1]) as fh:
		line=fh.readline()
		line=line.strip()
		ll=line.split('\t')
		lped=ll[0]
		for item in ll[1:6]:
			lped+='|'+item
		pedlist.append(lped)
		for j in range(6,len(ll)-1,2):
			pt=str(ll[j])+'|'+str(ll[j+1])
			pt_list.append(pt)
	for i in range(len(id_list)):
		out_d[id_list[i]]=[pt_list[i]]
	for start_nbr in range(1,int(len(file_list)/2)):
		sys.stdout.write('Starting file '+str(start_nbr+1)+'\n')
		sys.stdout.flush()
		id_list=[]
		pt_list=[]
		with open(file_list[int(2*start_nbr)]) as fh:
			for line in fh:
				id_list.append(line)
		with open(file_list[int(2*start_nbr+1)]) as fh:
			line=fh.readline()
			line=line.strip()
			ll=line.split('\t')
			lped=ll[0]
			for item in ll[1:6]:
				lped+='|'+item
			pedlist.append(lped)
			for j in range(6,len(ll)-1,2):
				pt=str(ll[j])+'|'+str(ll[j+1])
				pt_list.append(pt)
		for i in range(len(id_list)):
			if id_list[i] in out_d:
				out_d[id_list[i]].append(pt_list[i])
			else:
				out_d[id_list[i]]=['0|0']
				while len(out_d[id_list[i]])!=start_nbr:
					out_d[id_list[i]].append(['0|0'])	
				out_d[id_list[i]].append(pt_list[i])
		for key in out_d:
			if len(out_d[key]) != (start_nbr+1):
				out_d[key].append('0|0')
	return out_d, pedlist

def write_map(indict):
	with open('out.map','w') as fh:
		for key in indict:
			fh.write(key)

def write_ped(indict, lbl):
	import pandas as pd
	import csv
	outdf=pd.DataFrame(indict,
		index=lbl)
	Ω 
		sep='\t', 
		header=False, 
		quoting=csv.QUOTE_NONE)

def fix_ped():
	import os
	if os.path.exists('out2.ped'):
		os.remove('out2.ped')
	with open('out_tmp.ped') as fh:
		for line in fh:
			line=line.replace('|','\t')
			with open('out2.ped', 'a') as fh2:
				fh2.write(line)
	os.remove('out_tmp.ped')



if __name__ == '__main__':
	import sys
	ddd, labls=plink_merge(sys.argv[1])
	sys.stdout.write('Starting map write...\n')
	sys.stdout.flush()
	write_map(ddd)
	sys.stdout.write('Starting ped write...\n')
	sys.stdout.flush()
	write_ped(ddd, labls)
	sys.stdout.write('Fixing ped...\n')
	sys.stdout.flush()
	fix_ped()




lll=[]
for key in ddd:
	if len(ddd[key]) not in lll:
		lll.append(len(ddd[key]))








