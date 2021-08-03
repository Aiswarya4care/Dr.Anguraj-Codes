library(dplyr)
library(xlsx)
library(ggplot2)

#loading the data
df=read.xlsx("C:/Users/ash24/Downloads/QC_resampling.xlsx",1)
result= data.frame()

R=1000

for (i in c(2,7,8)){
  medslist1= c()
  medslist2= c()
  parameter=colnames(df)[i]
  quantile1=quantile(df[,i])
  med1= median(df[,i])
  
  for (j in 1:R){
    sample1= sample_n(df, round(0.67*nrow(df)))
    meds1= median(sample1[,i])
    medslist1= append(medslist1, meds1)
  }
  
  med1a= median(medslist1)
  ##subset after removing outliers
  
  subdf= df[(df[,i]>quantile1[[2]]),]
  quantile2=quantile(subdf[,i])
  med2= median(subdf[,i])
  
  for (k in 1:R){
    sample2= sample_n(subdf, round(0.67*nrow(subdf)))
    meds2= median(sample2[,i])
    medslist2= append(medslist2, meds2)
  }
  
  med2a= median(medslist2)
  
  row= c(parameter, med1,med1a ,quantile1[[1]],quantile1[[2]],quantile1[[3]],quantile1[[4]],quantile1[[5]],
         med2, med2a,quantile2[[1]],quantile2[[2]],quantile2[[3]],quantile2[[4]],quantile2[[5]] )
  
  result= rbind(result, row)
  print(parameter)
}

write.csv(result, "C:/Users/ash24/Desktop/results.csv")


