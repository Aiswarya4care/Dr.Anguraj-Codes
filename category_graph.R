library(dplyr)
library(ggplot2)
#loading the data
df=read.csv('/home/ash/Downloads/qcparameters.csv')
cols= colnames(df)

##### uniformity, uniquebase, mean target depth #############

for (j in 2:4){
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
df$sno= seq(1:nrow(df))
write.csv(df, "/home/ash/Downloads/qc1090.csv")

################## Plotting ######################

df= read.csv("updated1090.csv")

### Unique base enrichment ###########

df$Unique.base.enrichment
dec= quantile(df$Unique.base.enrichment, probs = seq(.1, .9, by = .1))

ggplot(df, aes(x=Unique.base.enrichment, y=sno, color=`qual Unique`)) +
  geom_point()+
  geom_rug()+
  ggtitle(label = "Unique.base.enrichment (10% and 90%)")+
  xlab("Unique.base.enrichment")+
  ylab("Uniformity of coverage")+
  geom_vline(xintercept=dec[[9]], color='darkgreen', size=0.5)+
  geom_vline(xintercept=dec[[1]], color='darkred', size=0.5)+
  labs(color = "Quality")


### Mean Target Depth ###########

df$`qual Mean`
dec= quantile(df$Mean.target.coverage.depth, probs = seq(.1, .9, by = .1))

ggplot(df, aes(x=Mean.target.coverage.depth, y=sno, color=`qual Mean`)) +
  geom_point()+
  geom_rug()+
  ggtitle(label = "Mean.target.coverage.depth (10% and 90%)")+
  xlab("Samples")+
  ylab("Mean.target.coverage.depth")+
  geom_vline(xintercept=dec[[9]], color='darkgreen', size=0.5)+
  geom_vline(xintercept=dec[[1]], color='darkred', size=0.5)+
  labs(color = "Quality")


### Uniformity ###########

df$`qual Uniformity`
dec= quantile(df$Uniformity.of.coverage..Pct...0.2.mean., probs = seq(.1, .9, by = .1))

ggplot(df, aes(x=Uniformity.of.coverage..Pct...0.2.mean., y=sno, color=`qual Uniformity`)) +
  geom_point()+
  geom_rug()+
  ggtitle(label = "Uniformity of coverage (10% and 90%)")+
  xlab("Samples")+
  ylab("Uniformity of coverage")+
  geom_vline(xintercept=dec[[9]], color='darkgreen', size=0.5)+
  geom_vline(xintercept=dec[[1]], color='darkred', size=0.5)+
  labs(color = "Quality")


######################## Duplicate #####################

j=5

col= df[,j]
qual=c()
dec= quantile(df[,j], probs = seq(.1, .9, by = .1))
for (k in 1:length(col)){
  
  para= col[k]
  
  bad= dec[[9]]
  good= dec[[1]]
  
  if (para>bad){
    qual= append(qual, "bad")
  } else if ( para<good) {
    qual= append(qual, "good")
  } else {
    qual= append(qual, "intermediate")
  }
  
  
}
df= cbind(df, qual)
names(df)[ncol(df)]=paste("qual", strsplit(cols[j],'[.]')[[1]][1])

### Plotting duplicate ######

df$`qual Percent`
dec= quantile(df$Percent.duplicate.aligned.reads, probs = seq(.1, .9, by = .1))

ggplot(df, aes(x=Percent.duplicate.aligned.reads, y=sno, color=`qual Percent`)) +
  geom_point()+
  geom_rug()+
  ggtitle(label = "Percent.duplicate.aligned.reads (10% and 90%)")+
  xlab("Samples")+
  ylab("Percent.duplicate.aligned.reads")+
  geom_vline(xintercept=dec[[1]], color='darkgreen', size=0.5)+
  geom_vline(xintercept=dec[[9]], color='darkred', size=0.5)+
  labs(color = "Quality")



