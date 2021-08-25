library(dplyr)
library(ggplot2)
#loading the data
df=read.csv('/home/ash/Downloads/qcparameters.csv')
cols= colnames(df)
output="/home/ash/Downloads"
############# 
parameters=c("Unique.base.enrichment","Mean.target.coverage.depth","Uniformity.of.coverage..Pct...0.2.mean.")

for (j in 1:length(cols)){
  if (cols[j] %in% parameters){
    col= df[,j]
    qual=c()
    dec= quantile(df[,j], probs = seq(.1, .9, by = .1))
    for (k in 1:length(col)){
      
      para= col[k]
      
      good= dec[[8]]
      bad= dec[[2]]
      
      if (para<bad){
        qual= append(qual, "bad")
      } else if ( para>good) {
        qual= append(qual, "good")
      } else {
        qual= append(qual, "intermediate")
      }
    }
    
    df= cbind(df, qual)
    names(df)[ncol(df)]=paste("qual", strsplit(cols[j],'[.]')[[1]][1])
  }
  
 
}

#####"Percent.duplicate.aligned.reads"

  col= df["Percent.duplicate.aligned.reads"][[1]]
  qual=c()
  dec= quantile(df["Percent.duplicate.aligned.reads"][[1]], probs = seq(.1, .9, by = .1))
  for (k in 1:length(col)){
    
    para= col[k]
    
    good= dec[[2]]
    bad= dec[[8]]
    
    if (para>bad){
      qual= append(qual, "bad")
    } else if ( para<good) {
      qual= append(qual, "good")
    } else {
      qual= append(qual, "intermediate")
    }
  }
  
  df= cbind(df, qual)
  names(df)[ncol(df)]=paste("qual", strsplit("Percent.duplicate.aligned.reads",'[.]')[[1]][1])

df$sno= seq(1:nrow(df))

################## Plotting ######################

### Unique base enrichment ###########

dec= quantile(df$Unique.base.enrichment, probs = seq(.1, .9, by = .1))

ggplot(df, aes(x=Unique.base.enrichment, y=sno, color=`qual Unique`)) +
  geom_point()+
  geom_rug()+
  ggtitle(label = "Unique.base.enrichment (20% and 80%)")+
  xlab("Unique.base.enrichment")+
  ylab("Samples")+
  geom_vline(xintercept=dec[[8]], color='darkgreen', size=0.5)+
  geom_vline(xintercept=dec[[2]], color='darkred', size=0.5)+
  annotate(geom="label",y=nrow(df)+20,x=c(dec[[8]],dec[[2]]),label=c(dec[[8]],dec[[2]]), fill="white")+
  labs(colour = "Quality")+
  coord_flip()+
  ylim(0,nrow(df)+30)

ggsave(paste0(output,"/uniquebase2080.png"))

### Mean Target Depth ###########

dec= quantile(df$Mean.target.coverage.depth, probs = seq(.1, .9, by = .1))

ggplot(df, aes(x=Mean.target.coverage.depth, y=sno, color=`qual Mean`)) +
  geom_point()+
  geom_rug()+
  ggtitle(label = "Mean.target.coverage.depth (20% and 80%)")+
  xlab("Mean.target.coverage.depth")+
  ylab("Samples")+
  geom_vline(xintercept=dec[[8]], color='darkgreen', size=0.5)+
  geom_vline(xintercept=dec[[2]], color='darkred', size=0.5)+
  annotate(geom="label",y=nrow(df)+20,x=c(dec[[8]],dec[[2]]),label=c(dec[[8]],dec[[2]]), fill="white")+
  labs(colour = "Quality")+
  coord_flip()+
  ylim(0,nrow(df)+30)


ggsave(paste0(output,"/meandepth2080.png"))

### Uniformity ###########

dec= quantile(df$Uniformity.of.coverage..Pct...0.2.mean., probs = seq(.1, .9, by = .1))

ggplot(df, aes(x=Uniformity.of.coverage..Pct...0.2.mean., y=sno, color=`qual Uniformity`)) +
  geom_point()+
  geom_rug()+
  ggtitle(label = "Uniformity of coverage (20% and 80%)")+
  xlab("Uniformity of coverage")+
  ylab("Samples")+
  geom_vline(xintercept=dec[[8]], color='darkgreen', size=0.5)+
  geom_vline(xintercept=dec[[2]], color='darkred', size=0.5)+
  annotate(geom="label",y=nrow(df)+20,x=c(dec[[8]],dec[[2]]),label=c(dec[[8]],dec[[2]]), fill="white")+
  labs(colour = "Quality")+
  coord_flip()+
  ylim(0,nrow(df)+30)


ggsave(paste0(output,"/uniformity2080.png"))

### Plotting duplicate ######

dec= quantile(df$Percent.duplicate.aligned.reads, probs = seq(.1, .9, by = .1))

ggplot(df, aes(x=Percent.duplicate.aligned.reads, y=sno, color=`qual Percent`)) +
  geom_point()+
  geom_rug()+
  ggtitle(label = "Percent.duplicate.aligned.reads (20% and 80%)")+
  xlab("Percent.duplicate.aligned.reads")+
  ylab("Samples")+
  geom_vline(xintercept=dec[[2]], color='darkgreen', size=0.5)+
  geom_vline(xintercept=dec[[8]], color='darkred', size=0.5)+
  annotate(geom="label",y=nrow(df)+20,x=c(dec[[8]],dec[[2]]),label=c(dec[[8]],dec[[2]]), fill="white")+
  labs(colour = "Quality")+
  coord_flip()+
  ylim(0,nrow(df)+30)


ggsave(paste0(output,"/perduplicate2080.png"))
############ writing
write.csv(df, "/home/ash/Downloads/qc2080.csv",row.names = FALSE)


