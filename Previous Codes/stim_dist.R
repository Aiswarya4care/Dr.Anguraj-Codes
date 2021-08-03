#This script contains the code for running stimulation and plotting the distribution
library(ggplot2)
library(dplyr)

data=read.csv("cohort_asian200.csv")

####################################################################
                #RUNNING STIMULATION FOR MEDIANS#
####################################################################

#creating an empty dataframe for recording stimulation values
stim=data.frame()

#no. of subset to be taken
n=round((2/3)*nrow(data))
R=500 #no. of simulations
  
#empty vector to record median values
med_all=c()

#loop for running the simulations
for (i in 1:R){
  random=sample_n(data,n) #selecting random n samples from the main dataset
  r_tmb=random[,3] #selecting column that has tmb values
  medall= median(r_tmb) #calculating median values for each sub sample
  med_all=append(med_all,medall) #creating vector with all median values
}

med_all=as.data.frame(med_all) #converting the vector to dataframe to for ggplot
med_all$ID= seq(1:R) #adding index for ggplot

####################################################################
                        #PLOTTING DISTRIBUTION#
####################################################################

m=round(mean(med_all$med_all),2)
se=round(sd(med_all$med_all),2)
cap=paste0("Abs.Median=",m," and ", "SD=", se)

dist=ggplot(med_all, aes(x=med_all,y=ID))+
  geom_point()+
  geom_rug()+
  labs(title="Distribution of medians R=500", caption=cap)+
  xlab("Medians")+
  ylab("Index")+
  xlim(1,15)+
  geom_vline(xintercept=m, color = "red", size=1)+
  geom_segment(aes(x = m-se, y = 0, xend = m+se, yend = 0),color = "red", size=1)

dist

####################################################################
                    #PLOTTING DISTRIBUTION#
####################################################################

cap=paste0("median= ",m, " and sd= ", se)
p8= deciles[9][[1]]
df <- data.frame(x =p8 , y1 = -0.4, y2 = 0.4)
ggplot(data, aes(x=TMB))+
  geom_boxplot(outlier.shape=NA)+
  labs(title="Box plot for raw TMB values", caption = cap)+
  ylab("TMB Values")+
  xlim(0,12)+
  ylim(-1,1)+
  geom_segment(aes(x = x, y = y1, xend = x, yend = y2, colour = "segment"),data = df)+
  annotate(geom="text", x=p8, y=0.6, label="Scatter plot",
           color="red")+
  coord_flip()


####################################################################
              #RUNNING STIMULATION FOR 8th DECILES#
####################################################################

#creating an empty dataframe for recording stimulation values
stim=data.frame()

#no. of subset to be taken
n=round((2/3)*nrow(data))
R=500 #no. of simulations

#empty vector to record median values
dec_all=c()

#loop for running the simulations
for (i in 1:R){
  random=sample_n(data,n) #selecting random n samples from the main dataset
  r_tmb=random[,4] #selecting column that has tmb values
  deciles=quantile(r_tmb,prob = seq(0, 1, length = 11), type = 5) #calculating deciles
  decall= deciles[9][[1]] #calculating decile values for each sub sample
  dec_all=append(dec_all,decall) #creating vector with all decile values
}

dec_all=as.data.frame(dec_all) #converting the vector to dataframe to for ggplot
dec_all$ID= seq(1:R) #adding index for ggplot

####################################################################
#PLOTTING DISTRIBUTION#
####################################################################

m=round(mean(dec_all$dec_all),2)
se=round(sd(dec_all$dec_all),2)
cap=paste0("Abs.Decile=",m," and ", "SD=", se)

dist=ggplot(dec_all, aes(x=dec_all,y=ID))+
  geom_point()+
  geom_rug()+
  labs(title="Distribution of deciles R=500", caption=cap)+
  xlab("Deciles")+
  ylab("Index")+
  xlim(1,30)+
  geom_vline(xintercept=m, color = "red", size=1)+
  geom_segment(aes(x = m-se, y = 0, xend = m+se, yend = 0),color = "red", size=1)

dist



