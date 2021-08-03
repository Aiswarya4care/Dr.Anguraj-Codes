library(ggplot2)
library(dplyr)
tmb_df=read.csv("C:/Users/ash24/Downloads/cohort_asian.csv")

#removing the outliers
tmbdf=sort(tmb_df$tmb)
tmbdf=data.frame(tmb=tmbdf)
tmbdf1=sort(tmb_df$tmb)
tmbdf1=data.frame(tmb=tmbdf1)[1:209,]
tmbdf1=data.frame(tmb=tmbdf1)


n= nrow(tmbdf)
quantiles=quantile(tmbdf$tmb)
deciles=quantile(tmbdf$tmb,prob = seq(0, 1, length = 11), type = 5)
quintiles=quantile(tmbdf$tmb,probs = seq(0, 1, 1/5))

n1= nrow(tmbdf1)
quantiles1=quantile(tmbdf1$tmb)
deciles1=quantile(tmbdf1$tmb,prob = seq(0, 1, length = 11), type = 5)
quintiles1=quantile(tmbdf1$tmb,probs = seq(0, 1, 1/5))


#Simple box plot with deciles

p8= deciles[9][[1]]
p81=deciles1[9][[1]]
df <- data.frame(x =p8 , y1 = -0.4, y2 = 0.4)
df1= data.frame(x =p81 , y1 = -0.4, y2 = 0.4)
ggplot(tmbdf, aes(x=tmb))+
  geom_boxplot(outlier.shape=NA)+
  labs(title="Box plot for TMB from Indian Cohort")+
  ylab(" ")+
  xlab("TMB Values")+
  xlim(0,12)+
  ylim(-1,1)+
  geom_segment(aes(x = x, y = y1, xend = x, yend = y2, colour = "8th Decile with outlier"),data = df)+
  annotate(geom="text", x=p8+0.5, y=0.5, label=round(p8,2),
           color="red")+
  geom_segment(aes(x = x, y = y1, xend = x, yend = y2, colour = "8th Decile without outlier"),data = df1)+
  annotate(geom="text", x=p81-0.5, y=0.5, label=round(p81,2),
           color="blue")+
  coord_flip()






