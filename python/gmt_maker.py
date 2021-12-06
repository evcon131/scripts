def gmt_maker(infile):
	th17up=[]
	th17down=[]
	th22up=[]
	th22down=[]
	th2up=[]
	th2down=[]
	Th1_17up=[]
	Th1_17down=[]
	Th1up=[]
	Th1down=[]
	Treg17up=[]
	Treg17down=[]
	Treg22up=[]
	Treg22down=[]
	Treg2up=[]
	Treg2down=[]
	Treg1_17up=[]
	Treg1_17down=[]
	Treg1up=[]
	Treg1down=[]
	pfccut=2
	nfccut=-2
	fdrcut=.05
	with open (infile) as fh:
		fh.readline()
		for line in fh:
			ll=line.split(",")
			gene=ll[0]
			if float(ll[2]) <=fdrcut:
				if float(ll[1]) > pfccut:
					th17up.append(gene)
				elif float(ll[1]) < nfccut:
					th17down.append(gene)
			if float(ll[4]) <=fdrcut:
				if float(ll[1]) > pfccut:
					th22up.append(gene)
				elif float(ll[1]) < nfccut:
					th22down.append(gene)
			if float(ll[6]) <=fdrcut:
				if float(ll[1]) > pfccut:
					th2up.append(gene)
				elif float(ll[1]) < nfccut:
					th2down.append(gene)
			if float(ll[8]) <=fdrcut:
				if float(ll[1]) > pfccut:
					Th1_17up.append(gene)
				elif float(ll[1]) < nfccut:
					Th1_17down.append(gene)
			if float(ll[10]) <=fdrcut:
				if float(ll[1]) > pfccut:
					Th1up.append(gene)
				elif float(ll[1]) < nfccut:
					Th1down.append(gene)
			if float(ll[12]) <=fdrcut:
				if float(ll[1]) > pfccut:
					Treg17up.append(gene)
				elif float(ll[1]) < nfccut:
					Treg17down.append(gene)
			if float(ll[14]) <=fdrcut:
				if float(ll[1]) > pfccut:
					Treg22up.append(gene)
				elif float(ll[1]) < nfccut:
					Treg22down.append(gene)
			if float(ll[16]) <=fdrcut:
				if float(ll[1]) > pfccut:
					Treg2up.append(gene)
				elif float(ll[1]) < nfccut:
					Treg2down.append(gene)
			if float(ll[18]) <= fdrcut:
				if float(ll[1]) > pfccut:
					Treg1_17up.append(gene)
				elif float(ll[1]) < nfccut:
					Treg1_17down.append(gene)
			if float(ll[20]) <= fdrcut:
				if float(ll[1]) > pfccut:
					Treg1up.append(gene)
				elif float(ll[1]) < nfccut:
					Treg1down.append(gene)
	outfile="th17_v_naive_up\tth17_v_naive_up"
	for item in th17up:
		outfile+="\t"+item
	outfile+="\n"
	outfile+="th17_v_naive_dn\tth17_v_naive_dn"
	for item in th17down:
		outfile+="\t"+item
	outfile+="\n"
	outfile+="th22_v_naive_up\tth22_v_naive_up"
	for item in th22up:
		outfile+="\t"+item
	outfile+="\n"
	outfile+="th22_v_naive_dn\tth22_v_naive_dn"
	for item in th22down:
		outfile+="\t"+item
	outfile+="\n"
	outfile+="th2_v_naive_up\tth2_v_naive_up"
	for item in th2up:
		outfile+="\t"+item
	outfile+="\n"
	outfile+="th2_v_naive_dn\tth2_v_naive_dn"
	for item in th2down:
		outfile+="\t"+item
	outfile+="\n"
	outfile+="Th1_17_v_naive_up\tTh1_17_v_naive_up"
	for item in Th1_17up:
		outfile+="\t"+item
	outfile+="\n"
	outfile+="Th1_17_v_naive_dn\tTh1_17_v_naive_dn"
	for item in Th1_17down:
		outfile+="\t"+item
	outfile+="\n"
	outfile+="th1_v_naive_up\tth1_v_naive_up"
	for item in Th1up:
		outfile+="\t"+item
	outfile+="\n"
	outfile+="th1_v_naive_dn\tth1_v_naive_dn"
	for item in Th1down:
		outfile+="\t"+item
	outfile+="\n"
	outfile+="Treg17_v_naive_up\tTreg17_v_naive_up"
	for item in Treg17up:
		outfile+="\t"+item
	outfile+="\n"
	outfile+="Treg17_v_naive_dn\tTreg17up_v_naive_dn"
	for item in Treg17down:
		outfile+="\t"+item
	outfile+="\n"
	outfile+="Treg22_v_naive_up\tTreg22_v_naive_up"
	for item in Treg22up:
		outfile+="\t"+item
	outfile+="\n"
	outfile+="Treg22_v_naive_dn\tTreg22up_v_naive_dn"
	for item in Treg22down:
		outfile+="\t"+item
	outfile+="\n"
	outfile+="Treg2_v_naive_up\tTreg2_v_naive_up"
	for item in Treg2up:
		outfile+="\t"+item
	outfile+="\n"
	outfile+="Treg2_v_naive_dn\tTreg2up_v_naive_dn"
	for item in Treg2down:
		outfile+="\t"+item
	outfile+="\n"
	outfile+="Treg1_17_v_naive_up\tTreg1_17_v_naive_up"
	for item in Treg1_17up:
		outfile+="\t"+item
	outfile+="\n"
	outfile+="Treg1_17_v_naive_dn\tTreg1_17up_v_naive_dn"
	for item in Treg1_17down:
		outfile+="\t"+item
	outfile+="\n"
	outfile+="Treg1_v_naive_up\tTreg1_v_naive_up"
	for item in Treg1up:
		outfile+="\t"+item
	outfile+="\n"
	outfile+="Treg1_v_naive_dn\tTreg1_v_naive_dn"
	for item in Treg1down:
		outfile+="\t"+item

	with open("out.gmt", "w") as fh:
		fh.write(outfile)

if __name__ == '__main__':
	import sys 
	gmt_maker(sys.argv[1])
