l=Sys.glob("*ReadsPerGene.out.tab")
cnt<-read.table(l[1],sep='\t')
d<-dim(cnt)
ncnt<-data.frame(cnt[5:d[1],3],row.names=cnt[5:d[1],1])
d<-length(l)
for (file in l[2:d]){
     holder<-read.table(file,sep='\t')
     d2<-dim(holder)
     d2<-d2[1]
     ncnt=cbind(ncnt,holder[5:d2[1],3])
 }
write.table(ncnt,file='combined_reads_raw_star.tab',sep='\t',col.names=F)
write.table(l,file='col_order_star.tab',sep='\t')

