def kar(infile):
	fh = open(infile)
	l=[]
	newline = ''
	for line  in fh:
		line = line.strip()
		line = line[3:]
		l.append(line.split('\t'))
	l2=[]
	test = 1
	for element in l:
		if element[0] != 'X':
			if int(element[0]) == test:
				l2.append(element)
				test+=1
	for element in l:
		if element[0] == 'X':
			l2.append(element) 
	#for element in l:
		#newline += 'chr '+'- '+'cf'+element[0]+' '+element[0]+' 0 '+element[1]+' chr'+element[0]+'\n'

	return l2
if __name__=='__main__':
	print(kar('chromInfo2.txt'))