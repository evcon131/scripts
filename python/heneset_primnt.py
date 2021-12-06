import sys
with open(sys.argv[1]) as fh:
	for line in fh:
		if sys.argv[2] in line:
			print(line)