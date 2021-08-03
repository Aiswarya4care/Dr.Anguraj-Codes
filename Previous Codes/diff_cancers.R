library(ggplot2)
library(dplyr)
#importing the prognostic dataset
diff=read.csv("cancers.csv")

#extracting the types of cancers
types= unique(diff$Cancer.type)

#empty vector to record median values
medians=data.frame()

#creating a dataframe with median values for each cancer type
for (i in 1:length(types)){
  type= types[i]
  median=round(median(diff[diff==type,]$TMB..mutations.Mb.),3)
  row=c(strsplit(type," ")[[1]][1],median)
  medians=rbind(medians,row)
}

#plotting the graph using ggplot
ggplot(diff, aes(x=Cancer.type, y=TMB..mutations.Mb.)) + 
  geom_boxplot()+
  xlab("Cancer type")+
  ylab("TMB Values")+
  labs(title = "Box Plot for TMB in different cancer types")+
  theme(axis.text.x = element_text(angle = 90))
