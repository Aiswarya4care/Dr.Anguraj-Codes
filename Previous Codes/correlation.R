library(ggplot2)

corr=read.csv("/home/bioinfoa/Documents/My Documents/TMB/Dr.Anguraj/Correlation/Files/lung.csv")
cancertype= "Liver"

cohort= corr[corr$data_type=="Cohort",]
c_med= round(median(cohort$tmb),3)
c_se= round(sd(cohort$tmb),3)
c_n= nrow(cohort)
cdeciles=quantile(cohort$tmb,prob = seq(0, 1, length = 11), type = 5)


public= corr[corr$data_type=="Public",]
p_med= round(median(public$tmb),3)
p_se= round(sd(public$tmb),3)
p_n= nrow(public)
pdeciles=quantile(public$tmb,prob = seq(0, 1, length = 11), type = 5)


cp8= cdeciles[9][[1]]
pp8= pdeciles[9][[1]]


#################################################################################################
              #Plotting the 8th decile#
#################################################################################################
ggplot(corr, aes(x= data_type, y=tmb)) + 
  geom_boxplot(width=0.5)+
 
  xlab(cancertype)+
  ylab("TMB Values")+
  ylim(1,18)+
  labs(title = "Correlation of TMB threshold values (8th decile)")+
  geom_segment(aes(x = 0.8, y = cp8, xend = 1.2, yend = cp8),color="darkgreen")+
  geom_segment(aes(x = 1.8, y = pp8, xend = 2.2, yend = pp8),color="blue")+
  annotate("text", x = 0.8, y = cp8+1, label = round(cp8,3))+
  annotate("text", x = 1.8, y = pp8+1, label = round(pp8,3))

#################################################################################################
            #Plotting the medians#
#################################################################################################

ggplot(corr, aes(x= data_type, y=tmb)) + 
  geom_boxplot(width=0.5)+
  
  xlab(cancertype)+
  ylab("TMB Values")+
  ylim(1,20)+
  labs(title = "Correlation of TMB threshold values (median)")+
  geom_segment(aes(x = 0.8, y = c_med, xend = 1.2, yend = c_med),color="darkgreen")+
  geom_segment(aes(x = 1.8, y = p_med, xend = 2.2, yend = p_med),color="blue")+
  annotate("text", x = 0.8, y = c_med+0.7, label = round(c_med,3))+
  annotate("text", x = 1.8, y = p_med+0.7, label = round(p_med,3))

