import glob
fqs=glob.glob('*')
fl=[]
defscript='#! /bin/bash\n#SBATCH --partition=shas\n#SBATCH --qos=normal \n#SBATCH -t 4:00:00\n#SBATCH -N 1\n#SBATCH --mail-type=END\n#SBATCH --mail-user=evan.conaway@gmail.com\ntrim_galore --paired '
for file in fqs:
    if '_1' in file:
        fl.append(file)
for file in fl:
    out=defscript
    out+=file+' '+file[0:-8]+'_2.fq.gz'
    outfh='ss'+file[0:-8]
    with open(outfh,'w') as ofh:
        ofh.write(out)
