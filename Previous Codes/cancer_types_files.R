cohort=read.csv("/home/bioinfoa/Documents/My Documents/TMB/Dr.Anguraj/cohort_asian200.csv")
public=read.csv("/home/bioinfoa/Documents/My Documents/TMB/Dr.Anguraj/cancers.csv")

#modifications to the file
cohort=cohort[,c(1,2,3)]
public=cbind(seq(1,nrow(public)),public)

#extracting cancer types for both datasets
coh_cancers= unique(cohort$Board.category)
pub_cancers=unique(public$Cancer.type)

#For colorectal cancers
col_coh= cohort[cohort$Board.category=="Colorectal",]
col_pub=public[public$Cancer.type=="Colorectal",]
col_coh$Board.category="Cohort"
col_pub$Cancer.type="Public"
colnames(col_coh)=c("ID","data_type","tmb")
colnames(col_pub)=c("ID","data_type","tmb")
colorectal=rbind(col_coh,col_pub)
write.csv(colorectal,"/home/bioinfoa/Documents/TMB/Dr.Anguraj/Correlation/colorectal.csv")


#For Lung cancer
lung_coh= cohort[cohort$Board.category=="Lung",]
lung_pub=rbind(public[public$Cancer.type=="NSCLC",],public[public$Cancer.type=="SCLC",])
lung_coh$Board.category="Cohort"
lung_pub$Cancer.type="Public"
colnames(lung_coh)=c("ID","data_type","tmb")
colnames(lung_pub)=c("ID","data_type","tmb")
lung=rbind(lung_coh,lung_pub)
write.csv(lung,"/home/bioinfoa/Documents/TMB/Dr.Anguraj/Correlation/lung.csv")

#For Breast Cancer
bre_coh= cohort[cohort$Board.category=="Breast",]
bre_pub=public[public$Cancer.type=="Breast",]
bre_coh$Board.category="Cohort"
bre_pub$Cancer.type="Public"
colnames(bre_coh)=c("ID","data_type","tmb")
colnames(bre_pub)=c("ID","data_type","tmb")
breast=rbind(bre_coh,bre_pub)
write.csv(breast,"/home/bioinfoa/Documents/TMB/Dr.Anguraj/Correlation/breast.csv")

#For liver cancer
liv_coh=cohort[cohort$Board.category=="Liver",]
liv_pub=public[public$Cancer.type=="Hepatobiliary",]
liv_coh$Board.category="Cohort"
liv_pub$Cancer.type="Public"
colnames(liv_coh)=c("ID","data_type","tmb")
colnames(liv_pub)=c("ID","data_type","tmb")
liver=rbind(liv_coh,liv_pub)
write.csv(liver,"/home/bioinfoa/Documents/My Documents/TMB/Dr.Anguraj/Correlation/liver.csv")



