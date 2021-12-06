def print_vartypes(infile):
	var_list=[]
	with open(infile) as fh:
		for line in fh:
			ll=line.split('\t')
			ll=ll[7].split('|')
			if ll[1] not in var_list:
				var_list.append(ll[1])
	for item in var_list:
		print(item)
if __name__ == '__main__':
	import sys
	print_vartypes(sys.argv[1])	