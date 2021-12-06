meta_data=data.frame(condition=c(rep.int('cd8',3),rep.int('new_cd4',4),rep.int('old_cd4',3), rep.int('tzn',7)),row.names=colnames(selct))
dds <- DESeqDataSetFromMatrix(countData =selct, colData = meta_data, design = ~ condition)
dds <- DESeq(dds)
res <- results(dds, contrast = c('condition','tzn','cd8'), tidy=T)
res2=results(dds, contrast = c('condition','tzn','new_cd4'), tidy = T)
res3=results(dds, contrast = c('condition','tzn','old_cd4'), tidy=T)
res[is.na(res$padj),7]=1
res2[is.na(res2$padj),7]=1
res3[is.na(res3$padj),7]=1
rownames(res)=res[,1]
rownames(res2)=res2[,1]
rownames(res3)=res3[,1]
res=res[,-1]
res2=res2[,-1]
res3=res3[,-1]
res=res[res$padj < .05 & !is.na(res$padj),]
res2=res2[res2$padj < .05 & !is.na(res2$padj),]
res3=res3[res3$padj < .05,]
cd8=rownames(res)
new_cd4=rownames(res2)
old_cd4=rownames(res3)
meta_data=data.frame(condition=c(rep.int('new_cntrl',3),rep.int('new_cntrl',4),rep.int('old_cntrl',3), rep.int('tzn',7)),row.names=colnames(selct))
dds <- DESeqDataSetFromMatrix(countData =selct, colData = meta_data, design = ~ condition)
dds <- DESeq(dds)
res <- results(dds, contrast = c('condition','tzn','new_cntrl'), tidy=T)
rownames(res)=res[,1]
res[is.na(res$padj),7]=1
res=res[,-1]
res=res[res$padj < .05,]
new_cntrl=rownames(res)
meta_data=data.frame(condition=c(rep.int('all_cntrl',3),rep.int('all_cntrl',4),rep.int('all_cntrl',3), rep.int('tzn',7)),row.names=colnames(selct))
dds <- DESeqDataSetFromMatrix(countData =selct, colData = meta_data, design = ~ condition)
dds <- DESeq(dds)
res <- results(dds, contrast = c('condition','tzn','all_cntrl'), tidy=T)
rownames(res)=res[,1]
res[is.na(res$padj),7]=1
res=res[,-1]
res=res[res$padj < .05,]
all_cntrl=rownames(res)
library(RColorBrewer)
alldata=list(cd8, new_cd4, old_cd4, new_cntrl, all_cntrl)
venn.diagram(
  x =  alldata,
  category.names = c("CD8" , "New\nCD4" , "Old CD4", "New\nControls", "All\nControls"),
  filename = 'contl_venn.tiff',
  output=TRUE,
  imagetype="tiff",
  col=brewer.pal(5, "Pastel2"),
  fill = brewer.pal(5, "Pastel2"))
