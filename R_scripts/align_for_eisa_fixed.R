library(QuasR)
library("BSgenome.Mmusculus.UCSC.mm10")

clObj <- makeCluster(2) # set the number of parallel processes
sampleFile1 <- "samplelist.txt"
proj <- qAlign(sampleFile1, "BSgenome.Mmusculus.UCSC.mm10", paired = "no", clObj= clObj)




# read file that provides an entrez gene id for each RefSeq transcript
trInfo <- read.delim("refLink_mm10_160615.txt",header=FALSE,as.is=TRUE)[,c(3,7)]
colnames(trInfo) <- c("RefSeqID","EntrezID")
rownames(trInfo) <- trInfo[,1]

# read the RefSeq transcript coordinates
genes <- read.delim("refGene_mm10_160615.txt",header=FALSE,stringsAsFactors=FALSE)
genes_to_nrLoci <- table(genes[,2]) # find transcripts that are at multiple loci in the genome
genes <- genes[genes[,2] %in% names(genes_to_nrLoci)[genes_to_nrLoci == 1],] # remove those transcripts
genes[,5] <- genes[,5]+1;genes[,7] <- genes[,7]+1; # convert to one based coordinates

# convert the trancript structures into an exon table
trToExonStartsL <- strsplit(genes[,10], ",")
trToExonEndsL <- strsplit(genes[,11], ",")
trToExonNr <- as.numeric(do.call(c,sapply(trToExonStartsL,function(x){1:length(x)})))
trToExonStartEnd <- data.frame(trId=rep(genes[,2],sapply(trToExonStartsL,length)),exonNr=trToExonNr,start=as.numeric(do.call(c,trToExonStartsL)),end=as.numeric(do.call(c,trToExonEndsL)))
trToExonStartEnd[,3] <- trToExonStartEnd[,3]+1 # convert to one based coordinates
trToGeneToExonStartEnd <- merge(trInfo,trToExonStartEnd,by.x=1,by.y=1)

exonInfo <- merge(trToGeneToExonStartEnd,genes[,2:4],by.x=1,by.y=1)
exonInfo_gr <- GRanges(seqnames = Rle(exonInfo[,6]),ranges = IRanges(exonInfo[,4], end = exonInfo[,5],names=exonInfo[,2]),strand=exonInfo[,7])

CO <- qCount(proj,exonInfo_gr,clObj= clObj) # count reads in exons

# select only protein coding genes
exonInfoE <- exonInfo[exonInfo[,1] %in% genes[genes[,8]-genes[,7] != -1,2],]

exonInfoE[,4] <- exonInfoE[,4] - 10 # extent the exons by 10 bp to make sure that reads close to the junctions are not counted as intronic
exonInfoE[,5] <- exonInfoE[,5] + 10

exonInfoE_gr <- GRanges(seqnames = Rle(exonInfoE[,6]),ranges = IRanges(exonInfoE[,4], end = exonInfoE[,5],names=exonInfoE[,2]),strand=exonInfoE[,7])

# determine the gene body coordinates for each gene
geneToMinStart <- aggregate(exonInfoE[,4],list(exonInfoE[,2]),min)
geneToMaxEnd <- aggregate(exonInfoE[,5],list(exonInfoE[,2]),max)
genebodyStartEnd <- merge(geneToMinStart,geneToMaxEnd,by.x=1,by.y=1)
gene_to_chr_strand <- aggregate(exonInfoE[,6:7],list(exonInfoE[,2]),function(x){x[1]})
genebody <- merge(genebodyStartEnd,gene_to_chr_strand,by.x=1,by.y=1)
genebody_gr <- GRanges(seqnames = Rle(genebody[,4]),ranges = IRanges(genebody[,2], end = genebody[,3],names=genebody[,1]),strand=genebody[,5])

CO_exonic <- qCount(proj,exonInfoE_gr,clObj= clObj) # count reads in extended (by 10bp) exons
CO_genebody <- qCount(proj,genebody_gr,clObj= clObj) # count reads in gene body (defined from 10bp extended exons)

# subtract exonic reads from the total gene body reads
CO_both <- merge(CO_exonic,CO_genebody,by.x=0,by.y=0)
rownames(CO_both) <- CO_both[,1]
CO_both <- as.matrix(CO_both[,-1])
CO_both <- CO_both[rownames(CO_exonic),]
CO_intronic <- CO_both[,(ncol(CO_exonic)+1):ncol(CO_both)] - CO_both[,1:ncol(CO_exonic)]
colnames(CO_intronic) <- colnames(CO_exonic)

write.table(CO_intronic,"expr_intronic.tab",sep="\t",quote=FALSE) # save intronic table
write.table(CO[rownames(CO_intronic),],"expr_mRNA.tab",sep="\t",quote=FALSE) # save exonic table with same gene order as intronic table

# find the genes that don't overlap with another one and save in a file for later use
genebody_overl <- countOverlaps(genebody_gr,genebody_gr) 
write.table(names(genebody_overl)[genebody_overl==1],"genes_not_overlapping.tab",sep="\t",quote=FALSE,row.names=FALSE,col.names=FALSE)

