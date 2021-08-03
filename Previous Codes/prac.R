library(dplyr)
library(xlsx)
library(ggplot2)
#loading the data
df=read.xlsx("C:/Users/ash24/Downloads/QC_resampling.xlsx",1)
df$sno= seq(1:nrow(df))

### first trial
quantile=quantile(df$Mean.target.coverage.depth)
p=ggplot(df, aes(x=Mean.target.coverage.depth,y=sno))+
  geom_point()+
  geom_rug()+
  labs(title="Distribution of Depth values")+
  xlab("Depth")+
  ylab("Index")+
  geom_vline(xintercept =quantile[[1]],color = "blue")+
  geom_vline(xintercept =quantile[[2]],color = "blue")+
  geom_vline(xintercept =quantile[[3]],color = "blue")+
  geom_vline(xintercept =quantile[[4]],color = "blue")


##################################################################

#second trial 5/4/21 - diff parameters
library(dplyr)
library(xlsx)
library(ggplot2)

#loading the data
df=read.xlsx("C:/Users/ash24/Downloads/QC_resampling.xlsx",1)
df$sno= seq(1:nrow(df))

result= data.frame("parameter","median before", "0%", "25%", "50%","75%","100%","median after removin outlier","median after resampling")
medslist= c()
R=1000

for (i in 2:ncol(df)){
  parameter=colnames(df)[i]
  med1= median(df[,i])
  subdf= df[df[,i]>med1,]
  quantile=quantile(subdf[,i])
  med2= median(subdf[,i])
  
  for (i in 1:R){
    sample= sample_n(subdf, round(0.67*nrow(subdf)))
    meds= median(sample$Percent.duplicate.aligned.reads)
    medslist= append(medslist, meds)
  }
 
  med3= median(medslist)
  
  row= c(parameter, med1, quantile[[1]],quantile[[2]],quantile[[3]],quantile[[4]],quantile[[5]],med2, med3)
  result= rbind(result, row)
  print(parameter)
}

write.csv(result, "C:/Users/ash24/Desktop/results.csv")


& (df[,i]<quantile1[[4]]))