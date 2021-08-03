library(ggplot2)
library(dplyr)

data=read.csv("cohort_asian200.csv")
colnames(data)=c("ID","cancertype","msi","tmb")
m=median(data$tmb)
se= round(sd(data$tmb),3)

####################################################################
                      #CALCULATING QUANTILES#
####################################################################
n= nrow(data)
quantiles=quantile(data$tmb)
deciles=quantile(data$tmb,prob = seq(0, 1, length = 11), type = 5)
quintiles=quantile(data$tmb,probs = seq(0, 1, 1/5))

####################################################################
                      #PLOTTING BOXPLOTS#
####################################################################

cap=paste0("median= ",m, " and sd= ", se)
p8= deciles[9][[1]]
df=data.frame(x =p8 , y1 = -0.4, y2 = 0.4)
box=ggplot(data, aes(x=tmb))+
  geom_boxplot(outlier.shape=NA)+
  labs(title="Box plot for raw TMB values", caption = cap)+
  ylab("TMB Values")+
  xlim(0,12)+
  ylim(-1,1)+
  geom_segment(aes(x = x, y = y1, xend = x, yend = y2, colour = "8th Decile with outlier"),data = df)+
  annotate(geom="text", x=p8+0.5, y=0.5, label=round(p8,2), color="red")+
  coord_flip()

print(box)


####################################################################
                      #PLOTTING DENSITY#
####################################################################

density= ggplot(data, aes(x=tmb)) + 
  geom_histogram(color="black", fill="white")+
  labs(title="Density Plot of TMB values", caption = cap)+
  xlab("TMB Values")+
  ylab("Count")+
  geom_vline(aes(xintercept=median(data$tmb)),color="red", linetype="dashed")

print(density)





