library(dplyr)
library(xlsx)
library(ggplot2)
#loading the data
df=read.xlsx("C:/Users/ash24/Downloads/resampling_QC_data.xlsx",2)

###### without removing outliers

results= data.frame()
for (i in 2:ncol(df)){
  parameter=colnames(df)[i]
  quantile1=quantile(df[,i])
  med= median(df[,i])
  row= c(parameter,med, quantile1[[1]],quantile1[[2]],quantile1[[3]],quantile1[[4]],quantile1[[5]])
  results= rbind(results, row)
}

##### removing below 25%
results= data.frame()
for (i in 2:ncol(df)){
  parameter=colnames(df)[i]
  quantile1=quantile(df[,i])
  subdf= df[(df[,i]>quantile1[[2]]),]
  quantile2=quantile(subdf[,i])
  med2= median(subdf[,i])
  row= c(parameter,med2,quantile2[[1]],quantile2[[2]],quantile2[[3]],quantile2[[4]],quantile2[[5]])
  results= rbind(results, row)
}

##### removing above 75%
results= data.frame()
for (i in 2:ncol(df)){
  parameter=colnames(df)[i]
  quantile1=quantile(df[,i])
  subdf= df[(df[,i]<quantile1[[4]]),]
  quantile2=quantile(subdf[,i])
  med2= median(subdf[,i])
  row= c(parameter,med2,quantile2[[1]],quantile2[[2]],quantile2[[3]],quantile2[[4]],quantile2[[5]])
  results= rbind(results, row)
}

##### removing below 25% and above 75%
results= data.frame()
for (i in 2:ncol(df)){
  parameter=colnames(df)[i]
  quantile1=quantile(df[,i])
  subdf= df[(df[,i]<quantile1[[4]] & df[,i]>quantile1[[2]]),]
  quantile2=quantile(subdf[,i])
  med2= median(subdf[,i])
  row= c(parameter,med2,quantile2[[1]],quantile2[[2]],quantile2[[3]],quantile2[[4]],quantile2[[5]])
  results= rbind(results, row)
}


write.csv(results, "/Users/ash24/Desktop/results.csv")
