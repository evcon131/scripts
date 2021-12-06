l=Sys.glob('*genes*')
cnt=read.delim(l[1],row.names=1)
colnames(cnt)[1]<-'transcript_id)s)'
colnames(cnt)[2]<-'length'
colnames(cnt)[3]<-'effective_length'
colnames(cnt)[4]<-'expected_count'
colnames(cnt)[5]<-'TPM'
colnames(cnt)[6]='FPKM'
d=length(l)
colnames(cnt)[5]=paste(colnames(cnt)[5],substr(l[1], start = 1, stop = nchar(l[1]) - 14), sep='_')
colnames(cnt)[6]=paste(colnames(cnt)[6],substr(l[1], start = 1, stop = nchar(l[1]) - 14), sep='_')
ncnt=cnt
for (file in l[2:d]){
	holder=read.delim(file,row.names=1)	
	colnames(holder)[5]=paste(colnames(holder)[5],substr(file, start = 1, stop = nchar(file) - 14), sep='_')
	colnames(holder)[6]=paste(colnames(holder)[6],substr(file, start = 1, stop = nchar(file) - 14), sep='_')
	ncnt=cbind(ncnt,holder[,5:6])
}
write.csv(ncnt,file='rsem_comb_counts.csv')
