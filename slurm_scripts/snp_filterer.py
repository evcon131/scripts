import glob
import time
stopet=0
intervals = (
    ('weeks', 604800),  # 60 * 60 * 24 * 7
    ('days', 86400),    # 60 * 60 * 24
    ('hours', 3600),    # 60 * 60
    ('minutes', 60),
    ('seconds', 1),
    )

def display_time(seconds, granularity=2):
    result = []

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(value, name))
    return ', '.join(result[:granularity])
cntrlsl=glob.glob('c*')
tzn='t1final.vcf'
out=''
cd={}
prgrss=0
total=0
strt=time.time()
fnlout=tzn+'out.vcf'
tznnow=tzn
progf=tzn+'_prog.txt'
for cfh1 in cntrlsl:
	with open(cfh1) as cfh:
		prgrss+=1
		if prgrss==1:
			with open(progf,'w') as pfh:
				pfh.write('starting c1...\n')
		if prgrss==2:
			with open(progf,'a') as pfh:
				pfh.write('starting c2...\n')
		for line in cfh:
			if '#' not in line[0]:
				ll=line.split('\t')
				if ll[0] not in cd:
					cd[ll[0]]=list(ll[1])
				if ll[0] in cd:
					cd[ll[0]].append(ll[1])
with open(progf,'a') as pfh:
	cnt_time=time.time()-strt
	pfh.write('Big Pizza! Control dictionary done in '+display_time(cnt_time)+' \nNow this next part is gonna take awhile better eat that pizza and get some suds\n')
#for tfh1 in tzn:
#if stopet>9000:
		#run_time=time.time()-strt
		#with open('progress_log2.txt','a') as pfh:
		#	pfh.write('Well that motherfucker took '+display_time(run_time) +'\n')
with open(progf,'a') as pfh:
	pfh.write('starting '+str(tznnow)+'\n')
with open(tzn) as tfh:
	ct=0
	stopet=9001
	strt=time.time()
	for line in tfh:
		if '#' not in line:
			ll=line.split('\t')
			ct+=1
			if ct % 10000 == 0:
				with open(progf,'a') as pfh:
					pfh.write('got '+str(ct)+' of these bitches done\n')
			if ll[1] not in cd[ll[0]]:
				if line not in out:
					out+=line
					total+=1
	with open(progf,'a') as pfh:
		pfh.write('Total SNPs written so far:  '+str(total)+'\n')	

with open('progf','a') as pfh:
	pfh.write('Total SNPs written   '+str(total)+'\n')	
with open(final,'w') as ofh:
	ofh.write(out)

