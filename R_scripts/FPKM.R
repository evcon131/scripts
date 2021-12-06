total_reads=colSums(finalres[,1:13])
res <- tail(finalres, 11)
res <- res[,1:13]
tcrs <- read.table('../tcrs.txt', sep='\t')
tcrs$exnl <- abs(tcrs$V5-tcrs$V4)
exl <- tcrs %>% 
  group_by(V9) %>% 
  summarize(thing = sum(exnl))
exl[,2] <- exl[,2] / 1000
total_reads <- total_reads / 1000000
res <- res / total_reads
res[1,] <- res[1,] / c(rep.int(exl[1,2],13))
