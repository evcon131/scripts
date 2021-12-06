library(AnnotationDbi)
library(org.Cf.eg.db)
library(biomaRt)
library(msigdbr)
library(enrichplot)
library(vroom)
library(tidyverse)
library(DESeq2)
library(clusterProfiler)
library(magrittr)
library(data.table)
library(clusterProfiler.dplyr)
setwd("~/Documents/Avery_lab/tzn_100annotation/remove1/cnts//")
filelist=Sys.glob("C*")
f1_counts<-read.table(filelist[1],sep='\t')
number_rows<-nrow(f1_counts)
raw_counts<-data.frame(f1_counts[5:number_rows,2])
rownames(raw_counts)<-f1_counts[5:number_rows,1]
colnames(raw_counts)[1]<-substr(filelist[1],start = 1, stop = nchar(filelist[1])-21)	
number_files<-length(filelist)
for (file in filelist[2:number_files]){
	holder<-read.table(file,row.names=1, sep='\t')
	colnames(holder)[1]<-substr(file,start = 1, stop = nchar(file)-21)	
	raw_counts<-merge(raw_counts,holder,by='row.names')
	rownames(raw_counts)<-raw_counts[,1]
	raw_counts<-raw_counts[,-1]
	number_columns<-ncol(raw_counts)
	raw_counts<-raw_counts[,-(number_columns)]
	raw_counts<-raw_counts[,-(number_columns-1)]
}
filelist=Sys.glob("T*")
for (file in filelist){
	holder<-read.table(file,row.names=1, sep='\t')
	colnames(holder)[3]<-substr(file,start = 1, stop = nchar(file)-21)	
	raw_counts<-merge(raw_counts,holder,by='row.names')
	rownames(raw_counts)<-raw_counts[,1]
	raw_counts<-raw_counts[,-1]
	number_columns<-ncol(raw_counts)
	raw_counts<-raw_counts[,-c((number_columns-2),(number_columns-1))]
}
raw_counts=raw_counts[,c(2:4,1,5:13)]
cd8cd4md=data.frame(condition=c(rep.int("cd8_cntrl",3),rep.int("cd4_control",4)), 
                    row.names=colnames(raw_counts[,1:7]))
tzncd8md=data.frame(condition=c(rep.int("cd8_cntrl",3),rep.int("tzn",6)), 
                    row.names=colnames(raw_counts[,c(1:3,8:13)]))
cd4md=data.frame(condition=c(rep.int("cd4_cntrl",4),rep.int("tzn",6)), 
                 row.names=colnames(raw_counts[,c(4:7,8:13)]))
cd8cd4dds=DESeqDataSetFromMatrix(countData = raw_counts[,1:7], 
                                 colData = cd8cd4md, 
                                 design = ~ condition)
cd8cd4dds<-DESeq(cd8cd4dds)
cd4dds=DESeqDataSetFromMatrix(countData = raw_counts[,c(4:13)], 
                              colData = cd4md, 
                              design = ~ condition)
tzncg8dds=DESeqDataSetFromMatrix(countData = raw_counts[,c(1:3,8:13)], 
                                 colData = tzncd8md, 
                                 design = ~ condition)
cd4dds<-DESeq(cd4dds)
tzncg8dds=DESeq(tzncg8dds)
res3=results(tzncg8dds, tidy=T)
res=results(cd4dds, tidy = T)
cres=results(cd8cd4dds, tidy = T)
rownames(res)=res[,1]
rownames(res3)=res3[,1]
rownames(cres)=cres[,1]
res=res[,-1]
res3=res3[,-1]
cres=cres[,-1]
alldmd=data.frame(condition=c(rep.int("cd8_cntrl",3),
                              rep.int("cd4_cntrl",4),
                              rep.int("tzn",6)), 
                  row.names=colnames(raw_counts))
alldds=DESeqDataSetFromMatrix(countData = raw_counts, 
                              colData = alldmd, 
                              design = ~ condition)
alldds=DESeq(alldds)
normc=counts(alldds, normalized=T)
finalres=merge(normc, res3, by="row.names")
rownames(finalres)=finalres[,1]
finalres=finalres[,-1]
finalres=merge(finalres, res, by="row.names")
rownames(finalres)=finalres[,1]
finalres=finalres[,-1]
finalres=finalres[,c(1:13,19,25)]
colnames(finalres)[14]="FDR_tzn_cd8"
colnames(finalres)[15]="FDR_tzn_cd4"
finalres$cd8_mean=rowMeans(finalres[,1:3])
finalres$cd4_mean=rowMeans(finalres[,4:7])
finalres$tzn_mean=rowMeans(finalres[,8:13])

finalres[finalres$cd8_mean==0,16]=1
finalres[finalres$cd4_mean==0,17]=1
finalres[finalres$tzn_mean==0,18]=1

finalres$l2fc_tzn_cd8=log2(finalres$tzn_mean / finalres$cd8_mean)
finalres$l2fc_tzn_cd4=log2(finalres$tzn_mean / finalres$cd4_mean)
finalres$l2fc_cd8_cd4=log2(finalres$cd8_mean / finalres$cd4_mean)

finalres=merge(finalres, cres, by="row.names")
rownames(finalres)=finalres[,1]
finalres=finalres[,-1]

finalres=finalres[,c(1:15,27,16:21)]

dog = useMart("ensembl", dataset = "clfamiliaris_gene_ensembl")
dogbm=getBM(attributes = c("ensembl_gene_id", "hgnc_symbol", "uniprot_gn_symbol"), mart = dog)
dens2hgncsym=function(ens){
  idx1 = which(dogbm$ensembl_gene_id == ens)
  if(length(idx1) == 0){return(NA)
  }else{
    sym = dogbm$hgnc_symbol[idx1[1]]
    return(sym)
      }
  }

dens2unisym=function(ens){
  idx1 = which(dogbm$ensembl_gene_id == ens)
  if(length(idx1) == 0){return(NA)
  }else{
    sym = dogbm$uniprot_gn_symbol[idx1[1]]
    return(sym)
      }
  }


finalres$symbol=mapIds(org.Cf.eg.db,keys = rownames(finalres),keytype = 'ENSEMBL', column = 'SYMBOL', multiVals = 'first')
finalres$uniprot_sym=sapply(rownames(finalres), FUN = dens2unisym, simplify = T, USE.NAMES = F)
finalres$hgnc_sym=sapply(rownames(finalres), FUN = dens2hgncsym, simplify = T, USE.NAMES = F)
for (i in 1:3){
    colnames(finalres)[i]<-paste("CD8",colnames(finalres)[i], sep="_")
}
for (i in 4:7){
    colnames(finalres)[i]<-paste("CD4",colnames(finalres)[i], sep="_")
}
colnames(finalres)[16] <- "FDR_cd8_cd4"
rm(i, file, cd8cd4dds, cd8cd4md, cres, alldds, alldmd, cd4dds, cd4md, dog, dogbm, f1_counts,holder, normc, raw_counts, res, res3,tzncd8md, tzncg8dds, number_columns, number_files, number_rows, filelist)


#GSEA

sigres=finalres[finalres$FDR_tzn_cd8<.05,]
#sigres=sigres[sigres$FDR_CD8_CD4>.05,]
sigres=sigres[!is.na(sigres$FDR_tzn_cd8),]
sigres <- sigres[abs(sigres$l2fc_tzn_cd8) > 1.5,]
sigres$entrez=mapIds(org.Cf.eg.db, 
                     keys=rownames(sigres), 
                     keytype = 'ENSEMBL', 
                     column = 'ENTREZID', 
                     multiVals = 'first')
s2nReturn=function (expmat, label) {
    freq <- table(label)
    if ((freq[1] < 2) || (freq[2] < 2)) {
        stop("There are not enough samples for calculating singal to noise ratio ya dingdong!")
    }
    x0 <- expmat[, which(label == 0)]
    x1 <- expmat[, which(label == 1)]
    m0 <- apply(x0, 1, mean)
    m1 <- apply(x1, 1, mean)
    sd0 <- apply(x0, 1, sd)
    sd1 <- apply(x1, 1, sd)
    s2n <- (m1 - m0)/(sd0 + sd1)
    return(s2n)
}
sigres <- sigres[!is.na(sigres$entrez),]
sigres$s2n=s2nReturn(sigres[,c(1:3,8:13)],c(0,0,0,1,1,1,1,1,1))
geneList=sigres$s2n
names(geneList)=as.character(sigres$entrez)
geneList <- sort(geneList, decreasing = TRUE)
geneList <- geneList[!duplicated(names(geneList))]
m_t2g <- msigdbr(species = "Canis lupus familiaris", category = "C7") %>% 
    dplyr::select(gs_name, entrez_gene)
em <- GSEA(geneList, 
            TERM2GENE = m_t2g, 
            eps=0, 
            pvalueCutoff = .01)
m_t2g <- msigdbr(species = "Canis lupus familiaris", category = "H") %>% 
    dplyr::select(gs_name, entrez_gene) 
em <- GSEA(geneList, TERM2GENE = m_t2g, pvalueCutoff = .01)
geneList=sigres$s2n
names(geneList)=as.character(sigres$uniprot_sym)
cell_markers <- vroom::vroom('http://bio-bigdata.hrbmu.edu.cn/CellMarker/download/Human_cell_markers.txt') %>%
  tidyr::unite("cellMarker", tissueType, cancerType, cellName, sep=", ") %>% 
  x <- DT::datatable(as.data.frame(cell_markers))
saveWidget(x, file = "source data.html")
cell_markers <- vroom::vroom('http://bio-bigdata.hrbmu.edu.cn/CellMarker/download/Human_cell_markers.txt') %>%
  tidyr::unite("cellMarker", tissueType, cancerType, cellName, sep=", ") %>% 
  dplyr::select(cellMarker, geneSymbol) %>%
  dplyr::mutate(geneSymbol = strsplit(geneSymbol, ', '))
gene <- names(geneList[geneList > 0])
em2 <- enricher(gene,
                TERM2GENE = cell_markers)
y <- enricher(gene, TERM2GENE=cell_markers, minGSSize=1)
x <- DT::datatable(as.data.frame(y))
saveWidget(x, file = "celltype gsea.html")

em2=setReadable(em, 'org.Cf.eg.db', 'ENTREZID')
em3 = filter(em2, !(Description %like% "KO"))
#em3 = filter(em3, !(Description %like% "_TREATED_"))
#em3 = filter(em3, !(Description %like% "_STIM_"))
em3 = filter(em3, !(Description %like% "_DC_"))
em3 = filter(em3, !(Description %like% "_TRANSDUCED_"))
#em3 = filter(em3, !(Description %like% "_CTRL_"))
em3 = filter(em3, !(Description %like% "_BCELL_"))
em3 = filter(em3, !(Description %like% "_MONOCYTE_"))
em3 = filter(em3, !(Description %like% "_NKTCELL_"))
#em3 = filter(em3, !(Description %like% "LSK"))
em3 = filter(em3, !(Description %like% "_DIABETIC_"))
#em3 = filter(em3, !(Description %like% "CXCR5"))
#em3 = filter(em3, !(Description %like% "BCL6"))
em3 = filter(em3, !(Description %like% "_NKT_"))
em3 = filter(em3, !(Description %like% "DELETED"))
em3 = filter(em3, !(Description %like% "SPLENOCYTES"))
em3 = filter(em3, !(Description %like% "BMDC"))
em3 = filter(em3, !(Description %like% "MACROPHAGE"))
em3 = filter(em3, !(Description %like% "_DEFICIENT")) 
em3 = filter(em3, !(Description %like% "MONOCYTE"))
em3 = filter(em3, !(Description %like% "KNOCKIN_"))
em3 = filter(em3, !(Description %like% "_SKIN_"))
em3 = filter(em3, !(Description %like% "NIH3T3"))
em3 = filter(em3, !(Description %like% "FUSION"))
em3 = filter(em3, !(Description %like% "MELANOMA"))
em3 = filter(em3, !(Description %like% "EPITHELIAL"))
em3 = filter(em3, !(Description %like% "_EOSINOPHIL_"))
em3 = filter(em3, !(Description %like% "_CDC_"))
em3 = filter(em3, !(Description %like% "ERYTHROD"))
em3 = filter(em3, !(Description %like% "MYELOD"))
em3 = filter(em3, !(Description %like% "_MICROGLIA_"))
em3 = filter(em3, !(Description %like% "MAST"))
em3 = filter(em3, !(Description %like% "IMPLANT"))
em3 = filter(em3, !(Description %like% "MAC"))
em3 = filter(em3, !(Description %like% "_PDC_"))
em3 = filter(em3, !(Description %like% "_EOSINOPHIL_"))
em3 = filter(em3, !(Description %like% "_NKCELL"))
em3 = filter(em3, !(Description %like% "_BMP_"))
em3 = filter(em3, !(Description %like% "MEF"))
em3 = filter(em3, !(Description %like% "_NEUTROPHIL"))
em3 = filter(em3, !(Description %like% "PBMC"))
em3 = filter(em3, !(Description %like% "BONE_MARROW"))
em3 = filter(em3, !(Description %like% "IRES"))
em3 = filter(em3, !(Description %like% "FR4NEG"))


em3@result$Description[-c(50,52,54,46,44,36,31,28,5,3)] <- substr(em3@result$Description[-c(50,52,54,46,44,36,31,28,5,3)], start = 10, 
	stop = nchar(em3@result$Description[-c(50,52,54,46,44,36,31,28,5,3)]))
em3@result$Description[c(50,52,54,46,44,31,28)] <- substr(em3@result$Description[c(50,52,54,46,44,41,28)], start = 9, 
	stop = nchar(em3@result$Description[c(50,52,54,46,44,31,28)]))
em3@result$Description <- str_replace_all(em3@result$Description, "_", " ")
em3@result$Description <- str_to_title(em3@result$Description)
em3@result$Description <- str_replace_all(em3@result$Description, "Up", "UP")
em3@result$Description <- str_replace_all(em3@result$Description, "Dn", "DN")
em3@result$Description <- str_replace_all(em3@result$Description, "Cd", "CD")

em3@result$Description <- str_replace_all(em3@result$Description, "Tgfbeta1", "TGFB1")
em3@result$Description <- str_replace_all(em3@result$Description, "Dp", "DP")
em3@result$Description <- str_replace_all(em3@result$Description, "Lcmv", "LCMV")
em3@result$Description <- str_replace_all(em3@result$Description, "Gd", "DN")
em3@result$Description <- str_replace_all(em3@result$Description, "Cxcr5", "CXCR5")
em3@result$Description <- str_replace_all(em3@result$Description, "Dss", "DSS")
em3@result$Description <- str_replace_all(em3@result$Description, "Tgfb", "TGFB")
em3@result$Description <- str_replace_all(em3@result$Description, "Bcl6", "BCL6")
em3@result$Description <- str_replace_all(em3@result$Description, "Il", "IL")
em3@result$Description <- str_replace_all(em3@result$Description, "Acd3", "ACD3")
em3@result$Description <- str_replace_all(em3@result$Description, "Pma", "PMA")
em3@result$Description <- str_replace_all(em3@result$Description, "Acd28", "ACD28")
em3@result$Description <- str_replace_all(em3@result$Description, "C57bl6", "C57BL6")
em3@result$Description <- str_replace_all(em3@result$Description, "Ifna", "IFNA")

pdf(file = "treg dot.pdf", width=11)
em3 %>% filter(Description %like% "TREG") %>%
dotplot(showCategory = 15, x = "NES") +
geom_vline(xintercept = 0, linetype=2)
dev.off()

pdf(file = "../c7 tznrm1 cs cd8s fdr<05 l2fc>1p5 dot.pdf", height = 12, width=12)
em2 %>%
  dotplot(showCategory = 49, x = "NES") +
  scale_colour_viridis_c(name = "Adjusted\nP-value") +
  geom_vline(xintercept = 0, linetype=2)
dev.off()

pdf(file = "GSE14415_ACT_TCONV_VS_ACT_NATURAL_TREG_UP.pdf")
gseaplot2(em3, 
          geneSetID = 'GSE14415_ACT_TCONV_VS_ACT_NATURAL_TREG_UP', 
          title = 'GSE14415_ACT_TCONV_VS_ACT_NATURAL_TREG_UP', 
          color = 'black') 
dev.off()

pdf(file = "GSE14415_ACT_VS_CTRL_NATURAL_TREG_UP.pdf")
gseaplot2(em3, 
          geneSetID = 'GSE14415_ACT_VS_CTRL_NATURAL_TREG_UP', 
          title = 'GSE14415_ACT_VS_CTRL_NATURAL_TREG_UP', 
          color = 'black') 
dev.off()






em4=em3 %>% slice(17,18)
fldlist=sigres$l2fc_tzn_cd8 
names(fldlist)=sigres$entrez

em4 = filter(em3, (Description %like% "MEMORY"))

pgls=vars$entrez
kk=enrichKEGG(gene=pgls, organism = "cfa", pvalueCutoff = .15)
kk <- setReadable(kk, 'org.Cf.eg.db', 'ENTREZDescription')
dotplot(kk, color="pvalue") + ggtitle(label = "KEGG Variant ORA")
dotplot(kk, color="p.adjust") + ggtitle(label = "KEGG Variant ORA")
sigres$hes=mapDescriptions(org.Hs.eg.db, keys = sigres$hs_sym, column = "ENTREZDescription", keytype = "SYMBOL")
geneList=sigres$s2n
names(geneList)=sigres$hes
geneList <- sort(geneList, decreasing = TRUE)

noparasgenes=vars[vars$paralog_eDescription=="", "entrez"]
ego3 <- enrichGO(gene         = noparasgenes,
                 OrgDb         = org.Cf.eg.db,
                 
                 ont           = "ALL",
                 pAdjustMethod = "BH",
                 pvalueCutoff  = 0.2,
                 qvalueCutoff  = 0.2)
geneList=sigres$s2n
names(geneList)=sigres$entrez
geneList <- sort(geneList, decreasing = TRUE)
kk2 <- gseKEGG(geneList     = geneList,
              organism     = 'cfa',
              minGSSize    = 3,
              maxGSSize    = 800)
kk2 <- setReadable(kk2, 'org.Cf.eg.db', 'ENTREZID')

#vars and paraligs
var2=read.table("final_results_newpipi/condensd_vcf.tab", sep="\t", header = T)
library(biomaRt)
ensembl=useMart("ensembl")
dog = useMart("ensembl", dataset = "clfamiliaris_gene_ensembl", host = "uswest.ensembl.org")
dogBM = getBM(attributes = c("ensembl_gene_Description","clfamiliaris_paralog_ensembl_gene"),mart = dog)
paralogchecker = function(ens)
{
  Descriptionx1 = which(dogBM$ensembl_gene_Description == ens)
  if(length(Descriptionx1) == 0){return(NA)
  }else{
    pl = dogBM$clfamiliaris_paralog_ensembl_gene[Descriptionx1[1]]
    return(pl)
      }
  }
var2$paralog_eDescription = sapply(as.character(var2$geneDescription), FUN = paralogchecker, simplify = T, USE.NAMES = F)
var2$para_symbol=mapDescriptions(org.Cf.eg.db,keys = as.character(var2$paralog_eDescription),keytype = 'ENSEMBL', column = 'SYMBOL', multiVals = 'first')
var2$para_uniprot_sym=sapply(as.character(var2$paralog_eDescription), FUN = dens2unisym, simplify = T, USE.NAMES = F)
var2$para_hgnc_sym=sapply(as.character(var2$paralog_eDescription), FUN = dens2hgncsym, simplify = T, USE.NAMES = F)
var3=merge(var2, finalres, all.x=T, by.x="paralog_eDescription", by.y="row.names" )
var3=var3[,-c(24:37,47:50)]
for (i in 23:31){
    colnames(var3)[i]<-paste("para",colnames(var3)[i], sep="_")
}
var4=merge(var3, finalres, by.x="geneDescription", by.y="row.names", all.x = T)
var4=var4[,-c(32:45,55:58)]
for (i in c(1,3,32:40)){
    colnames(var4)[i]<-paste("og_variant",colnames(var4)[i], sep="_")
}




