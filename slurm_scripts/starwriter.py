import glob
fqs=glob.glob('T*')
fl=[]
def1='#! /bin/bash\n#SBATCH --partition=shas\n#SBATCH --qos=normal \n#SBATCH -t 6:00:00\n#SBATCH -N 1\n#SBATCH --mail-type=END\n#SBATCH --mail-user=evan.conaway@gmail.com\n#SBATCH --mem=60000\n/projects/evcon\@colostate.edu/STAR-2.5.3a/bin/Linux_x86_64/STAR \\\n--genomeDir /projects/evcon@colostate.edu/str_dep/str_idx \\\n--outSAMtype BAM SortedByCoordinate \\\n--quantMode GeneCounts \\\n--sjdbGTFfile /projects/evcon@colostate.edu/str_dep/cf3gtf.gtf \\\n--outFilterMultimapNmax 1 \\\n--readFilesCommand zcat \\\n--outFileNamePrefix '
def2=' \\\n--readFilesIn '
for file in fqs:
    if '_1' in file:
        fl.append(file)
for file in fl:
    out=def1
    out+=file[0:-14]+def2
    out+=file+' '+file[0:-14]+'_2_val_2.fq.gz'
    outfh='ss'+file[0:-8]
    with open(outfh,'w') as ofh:
        ofh.write(out)
