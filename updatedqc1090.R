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
      
      good= dec[[9]]
      bad= dec[[1]]
      
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
  
  good= dec[[1]]
  bad= dec[[9]]
  
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
  ggtitle(label = "Unique.base.enrichment (10% and 90%)")+
  xlab("Unique.base.enrichment")+
  ylab("Samples")+
  geom_vline(xintercept=dec[[9]], color='darkgreen', size=0.5)+
  geom_vline(xintercept=dec[[1]], color='darkred', size=0.5)+
  annotate(geom="label",y=nrow(df)+20,x=c(dec[[9]],dec[[1]]),label=c(dec[[9]],dec[[1]]), fill="white")+
  labs(colour = "Quality")+
  coord_flip()+
  ylim(0,nrow(df)+30)


ggsave(paste0(output,"/uniquebase1090.png"))

### Mean Target Depth ###########

dec= quantile(df$Mean.target.coverage.depth, probs = seq(.1, .9, by = .1))

ggplot(df, aes(x=Mean.target.coverage.depth, y=sno, color=`qual Mean`)) +
  geom_point()+
  geom_rug()+
  ggtitle(label = "Mean.target.coverage.depth (10% and 90%)")+
  xlab("Mean.target.coverage.depth")+
  ylab("Samples")+
  geom_vline(xintercept=dec[[9]], color='darkgreen', size=0.5)+
  geom_vline(xintercept=dec[[1]], color='darkred', size=0.5)+
  annotate(geom="label",y=nrow(df)+20,x=c(dec[[9]],dec[[1]]),label=c(dec[[9]],dec[[1]]), fill="white")+
  labs(colour = "Quality")+
  coord_flip()+
  ylim(0,nrow(df)+30)


ggsave(paste0(output,"/meandepth1090.png"))

### Uniformity ###########

dec= quantile(df$Uniformity.of.coverage..Pct...0.2.mean., probs = seq(.1, .9, by = .1))

ggplot(df, aes(x=Uniformity.of.coverage..Pct...0.2.mean., y=sno, color=`qual Uniformity`)) +
  geom_point()+
  geom_rug()+
  ggtitle(label = "Uniformity of coverage (10% and 90%)")+
  xlab("Uniformity of coverage")+
  ylab("Samples")+
  geom_vline(xintercept=dec[[9]], color='darkgreen', size=0.5)+
  geom_vline(xintercept=dec[[1]], color='darkred', size=0.5)+
  annotate(geom="label",y=nrow(df)+20,x=c(dec[[9]],dec[[1]]),label=c(dec[[9]],dec[[1]]), fill="white")+
  labs(colour = "Quality")+
  coord_flip()+
  ylim(0,nrow(df)+30)


ggsave(paste0(output,"/uniformity1090.png"))

### Plotting duplicate ######

dec= quantile(df$Percent.duplicate.aligned.reads, probs = seq(.1, .9, by = .1))

ggplot(df, aes(x=Percent.duplicate.aligned.reads, y=sno, color=`qual Percent`)) +
  geom_point()+
  geom_rug()+
  ggtitle(label = "Percent.duplicate.aligned.reads (10% and 90%)")+
  xlab("Percent.duplicate.aligned.reads")+
  ylab("Samples")+
  geom_vline(xintercept=dec[[1]], color='darkgreen', size=0.5)+
  geom_vline(xintercept=dec[[9]], color='darkred', size=0.5)+
  annotate(geom="label",y=nrow(df)+20,x=c(dec[[9]],dec[[1]]),label=c(dec[[9]],dec[[1]]), fill="white")+
  labs(colour = "Quality")+
  coord_flip()+
  ylim(0,nrow(df)+30)


ggsave(paste0(output,"/perduplicate1090.png"))
############ writing
write.csv(df, "/home/ash/Downloads/qc1090.csv",row.names = FALSE)


