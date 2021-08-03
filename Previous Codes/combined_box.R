library(ggplot2)
library(dplyr)
col=read.csv("C:/Users/ash24/Downloads/Book2.csv")
mcohort=round(median(col[col$cancer=="Cohort",]$v7),2)
mcol=round(median(col[col$cancer=="Colorectal",]$v7),2)
mnon=round(median(col[col$cancer=="Non Colorectal",]$v7),2)

ggplot(col, aes(x=cancer, y=v7)) + 
  geom_boxplot()+
  xlab("Cancer type")+
  ylab("TMB Values")+
  labs(title = "Box Plot for TMB based on cancer type")+
  annotate(geom="text", x=1, y=mcohort+1, label=mcohort,
           color="red")+
  annotate(geom="text", x=2, y=mcol+1, label=mcol,
           color="red")+
  annotate(geom="text", x=3, y=mnon+1, label=mnon,
           color="red")

###### Different cancer types









 