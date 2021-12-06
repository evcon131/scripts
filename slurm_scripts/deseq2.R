setwd('Documents/Avery_lab/tzone/anlysis/round2/')
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
write.csv(ncnt,file='counts_RAW.csv')
library(DESeq2)
colnames(ncnt)=c('c1','c2','c3','t1','t2','t3','t4','t5','t6','t7')
col=data.frame(condition=c('c','c','c','t','t','t','t','t','t','t'),row.names=c('c1','c2','c3','t1','t2','t3','t4','t5','t6','t7'))
dds <- DESeqDataSetFromMatrix(countData =ncnt, colData = col, design = ~ condition)
#removes rows with < 10 counts
keep <- rowSums(counts(dds)) >= 10
dds <- dds[keep,]
dds$condition <- factor(dds$condition, levels = c("c","t"))
dds <- DESeq(dds)
res <- results(dds)
res$sym<-mapIds(org.Cf.eg.db,keys=rownames(res),keytype="ENSEMBL",column="SYMBOL",multiVals="first")
write.csv(res,file='result]final.csv',quote=F)
write.csv(counts(dds,normalized=TRUE),file='counts_normilized.csv')


