import pandas as pd
import numpy as np
import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

window=tk.Tk()
 
# setting the windows size
window.geometry("600x500")
window.title("Patient Data Processing")  
# declaring string variab nle
library_kit=tk.StringVar()
location_name=tk.StringVar()
project= tk.StringVar()
folderPath=tk.StringVar()
appsession_name=tk.StringVar()

def browse():
    folder_selected = filedialog.askdirectory()
    folderPath.set(folder_selected)
    
def submit():
    
 #retrieving sample name
    location = folderPath.get()
    file_list=os.listdir(location)
    if 'temp1.sh' in file_list:
        os.system("rm " + location + "/temp1.sh")
    if 'cutadaptlog' in file_list:
        os.system("rm " + location + "/cutadaptlog")
#kit chosen and retrieving adapters 
    libkit=library_kit.get()
    if libkit=="Roche":
        adapter="AGATCGGAAGAGC"
    elif libkit=="Illumina":
        adapter="CTGTCTCTTATACACATCT"
    else:
        adapter="AGATCGGAAGAGC"

#project selection and project id retrieval
    proj= project.get()
    if proj=="Somatic DNA":
        vctype="1"
        pid="175429254"
    elif proj=="Somatic RNA":
        pid="148206064"
    else:
        pid="166558401"
        vctype="0"

    l1="for i in *_R1.fastq.gz"
    l2="do"
    l3="   SAMPLE=$(echo ${i} | sed \"s/_R1\.fastq\.gz//\") "
    l4="   echo ${SAMPLE}_R1.fastq.gz ${SAMPLE}_R2.fastq.gz"
    l5="   cutadapt -j 30 -m 35 -a "+ adapter +" -A " +adapter+" -o ${SAMPLE}_S1_L001_R1_001.fastq.gz -p ${SAMPLE}_S1_L001_R2_001.fastq.gz ${SAMPLE}_R1.fastq.gz ${SAMPLE}_R2.fastq.gz >" + location + "/cutadaptlog" + "/${SAMPLE}_cutadaptlog.txt"
    l6="done"
    l8="bs upload dataset --project="
    l10="echo \"############ FQ and CA completed ###########\""
    
    os.system("mkdir "+ location+ "/cutadaptlog")
    temp= location + "/temp1.sh"
    f= open(temp,"x")
    f.close()
    f= open(temp,"w+")
    f.write("cd " + location)
    f.write('\n' + l1)
    f.write('\n' + l2)
    f.write('\n' + l3)
    f.write('\n' + l4)
    f.write('\n' + l5)
    f.write('\n' + l6)
    f.write('\n'+ l8 + str(pid) + " *R1_001.fastq.gz *R2_001.fastq.gz")
    f.write('\n' + l10)
    f.close()
    
    ###location and info
    print("################################")
    print("######### INFORMATION ##########")
    print("################################")
    print("Selected Project is " + str(proj))
    print("Project ID is " + str(pid))
    print("Adapter information: " + str(adapter))
    print("Data located in: " + str(location))
    print("No. of files selected is " + str(len(os.listdir(location))-2))
    a = ("Selected Project is " +
       str(proj) + "\n" +
       "Project ID is " +
       str(pid) + "\n" +
       "Data located in: "+
       str(location))
    answer = tk.messagebox.askyesnocancel("Confirmation", a)
    if answer:
        print("################################")
        print("############ Running FQ and Cutadapt ###########")
        print("################################")
        location= folderPath.get()
        temp1_path= location + "/" + "temp1.sh"
        os.system("sh " + temp1_path)
        print("################################")
        print("############ Done ###########")
        print("################################")
    else:
        rm_cmd=" rm "+ location + "/" + "temp1.sh"
        os.system(rm_cmd) 
        
############ running from fq cutadapt to till dragen launch ############
      
def together():
       
#retrieving sample name
    location = folderPath.get()
    file_list=os.listdir(location)
    if 'cutadaptlog' in file_list:
        os.system("rm " + location + "/cutadaptlog")
    if 'temp1.sh' in file_list:
        os.system("rm " + location + "/temp1.sh")
    libkit=library_kit.get()
    proj= project.get()
    appsess= appsession.get()
    samples=[]
    for file in file_list:
        sample= file.split("_")
        samples.append(sample[0])
    samples= pd.unique(samples)
    samples=np.array(samples).tolist()
    
    if 'temp1.sh' in samples:
        samples.remove('temp1.sh')
    if 'panel' in samples:
        samples.remove('panel')
    if 'panellog.txt' in samples:
        samples.remove('panellog.txt')
    if 'cutadaptlog.txt' in samples:    
        samples.remove('cutadaptlog.txt')
    if 'FQlog.txt' in samples:    
        samples.remove('FQlog.txt')
    if 'MSI' in samples:
        samples.remove('MSI')
    if 'CNV' in samples:
        samples.remove('CNV')
    if 'cutadaptlog' in samples:
        samples.remove('cutadaptlog')   
#kit chosen and retrieving adapters 
    libkit=library_kit.get()
    if libkit=="Roche":
        adapter="AGATCGGAAGAGC"
        bed_file_loc= "roche_hg19_panel.bed"
    elif libkit=="Illumina":
        adapter="CTGTCTCTTATACACATCT"
        bed_file_loc="CEX_illumina_nextera_panel.bed"
    else:
        adapter="AGATCGGAAGAGC"
        bed_file_loc="New_agilent_panel.bed"

#project selection and project id retrieval
    proj= project.get()
    if proj=="Somatic DNA":
        vctype="1"
        pid="175429254"
        proj_des="Somatic_Patient_Samples"
    elif proj=="Somatic RNA":
        pid="148206064"
    else:
        pid="166558401"
        vctype="0"
        proj_des="Germline_Patient_Sample"

#command for dragen
    if libkit=="Illumina" and proj=="Somatic DNA":
        cmd="bs launch application -n \"DRAGEN Enrichment\" --app-version 3.6.3 -o app-session-name:"+ appsess +" -l " + appsess +" -o project-id:175429254 -o vc-type:1 -o annotation-source:ensembl -o ht-ref:hg19-altaware-cnv-anchor.v8 -o fixed-bed:Illumina_Exome_TargetedRegions_v1.2 -o qc-coverage-region-padding-2:150 -o input_list.sample-id:$bsids -o picard_checkbox:1 -o vc-af-call-threshold:5 -o vc-af-filter-threshold:10 -o sv_checkbox:1 -o commandline-disclaimer:true"
    
    if libkit=="Illumina" and proj=="Germline":
        cmd="bs launch application -n \"DRAGEN Enrichment\" --app-version 3.6.3 -o app-session-name:"+ appsess +" -l "+ appsess +" -o project-id:166558401 -o vc-type:0 -o annotation-source:ensembl -o ht-ref:hg19-altaware-cnv-anchor.v8 -o fixed-bed:Illumina_Exome_TargetedRegions_v1.2 -o qc-coverage-region-padding-2:150 -o input_list.sample-id:$bsids -o picard_checkbox:1 -o sv_checkbox:1 -o commandline-disclaimer:true"

    if libkit=="Agilent" and proj=="Somatic DNA":
        bed_id=20024037150
        cmd= "bs launch application -n \"DRAGEN Enrichment\" --app-version 3.6.3 -o app-session-name:"+ appsess +" -l "+ appsess +" -o project-id:175429254 -o vc-type:1 -o annotation-source:ensembl -o ht-ref:hg19-altaware-cnv-anchor.v8 -o fixed-bed:custom -o target_bed_id:"+ str(bed_id) +" -o qc-coverage-region-padding-2:150 -o input_list.sample-id:$bsids -o picard_checkbox:1 -o vc-af-call-threshold:5 -o vc-af-filter-threshold:10 -o sv_checkbox:1 -o commandline-disclaimer:true"
    
    if libkit=="Agilent" and proj=="Germline":
        bed_id=20024037150        
        cmd="bs launch application -n \"DRAGEN Enrichment\" --app-version 3.6.3 -o app-session-name:"+ appsess +" -l "+ appsess +" -o project-id:166558401 -o vc-type:0 -o annotation-source:ensembl -o ht-ref:hg19-altaware-cnv-anchor.v8 -o fixed-bed:custom -o target_bed_id:"+ str(bed_id) +" -o qc-coverage-region-padding-2:150 -o input_list.sample-id:$bsids -o picard_checkbox:1 -o sv_checkbox:1 -o commandline-disclaimer:true"

    if libkit=="Roche" and proj=="Somatic DNA":
        bed_id=20977118310
        cmd= "bs launch application -n \"DRAGEN Enrichment\" --app-version 3.6.3 -o app-session-name:"+ appsess +" -l "+ appsess +" -o project-id:175429254 -o vc-type:1 -o annotation-source:ensembl -o ht-ref:hg19-altaware-cnv-anchor.v8 -o fixed-bed:custom -o target_bed_id:"+ str(bed_id) +" -o qc-coverage-region-padding-2:150 -o input_list.sample-id:$bsids -o picard_checkbox:1 -o vc-af-call-threshold:5 -o vc-af-filter-threshold:10 -o sv_checkbox:1 -o commandline-disclaimer:true"

    if libkit=="Roche" and proj=="Germline":
        bed_id=20977118310        
        cmd="bs launch application -n \"DRAGEN Enrichment\" --app-version 3.6.3 -o app-session-name:"+ appsess +" -l "+ appsess +" -o project-id:166558401 -o vc-type:0 -o annotation-source:ensembl -o ht-ref:hg19-altaware-cnv-anchor.v8 -o fixed-bed:custom -o target_bed_id:"+ str(bed_id) +" -o qc-coverage-region-padding-2:150 -o input_list.sample-id:$bsids -o picard_checkbox:1 -o sv_checkbox:1 -o commandline-disclaimer:true"
    
    if proj=="Somatic RNA":
        cmd="bs launch application -n \"DRAGEN RNA Pipeline\" --app-version 3.6.3 -o app-session-name:"+ appsess +" -l "+ appsess +" -o project-id:148206064 -o sample-id:$bsids -o ht-ref:hg19-altaware-cnv-anchor.v8 -o gene_fusion:1 -o quantification_checkbox:0 -o commandline-disclaimer:true"
    
#for dragen 
    
    
    l2="for i in *_R1.fastq.gz"
    l3="do"
    l4="   SAMPLE=$(echo ${i} | sed \"s/_R1\.fastq\.gz//\") "
    l5="   echo ${SAMPLE}_R1.fastq.gz ${SAMPLE}_R2.fastq.gz"
    l6="   cutadapt -j 30 -m 35 -a "+ adapter +" -A " +adapter+" -o ${SAMPLE}_S1_L001_R1_001.fastq.gz -p ${SAMPLE}_S1_L001_R2_001.fastq.gz ${SAMPLE}_R1.fastq.gz ${SAMPLE}_R2.fastq.gz >" + location + "/cutadaptlog" + "/${SAMPLE}_cutadaptlog.txt"
    l7="done"
    l8="bs upload dataset --project="
    l10="samples=(" + str(samples).strip("[]").replace("'","").replace(",","") + ")"
    l11="for i in ${samples[@]};  do"
    l12="echo $i;"
    l13="bsid=`bs get biosample -n $i –terse | grep \"Id\" | head -1 | grep -Eo '[0-9]{1,}'`;"
    l14="bsids+=($bsid)"
    l15="done"
    l16="printf -v joined '%s,' \"${bsids[@]}\""
    l17="bsids=${joined%,}"
    l18="echo $bsids"
    l1="perl /home/basecare/Programs/fastqc_v0.11.9/FastQC/fastqc *.gz"
    
    os.system("mkdir "+ location+ "/cutadaptlog")
    temp= location + "/temp1.sh"
    f= open(temp,"x")
    f.close()
    f= open(temp,"w+")
    f.write("cd " + location)
    f.write('\n' + l2)
    f.write('\n' + l3)
    f.write('\n' + l4)
    f.write('\n' + l5)
    f.write('\n' + l6)
    f.write('\n' + l7)
    f.write('\n'+ l8 + str(pid) + " *R1_001.fastq.gz *R2_001.fastq.gz")
    f.write('\n' + l10)
    f.write('\n' + l11)
    f.write('\n' + l12)
    f.write('\n' + l13)
    f.write('\n' + l14)
    f.write('\n' + l15)
    f.write('\n' + l16)
    f.write('\n'+l17)
    f.write('\n'+l18)
    f.write('\n'+ cmd)
    f.write('\n'+"echo \"########################\"")
    f.write('\n'+"echo \"Dragen Launched\"")
    f.write('\n'+"echo \"########################\"")
    f.write('\n' + l1)
    f.write('\n'+"echo \"########################\"")
    f.write('\n'+"echo \"FastQC completed\"")
    f.write('\n'+"echo \"########################\"")
    f.close()
 ###location and info
    print("################################")
    print("######### INFORMATION ##########")
    print("################################")
    print("Selected Project is " + str(proj))
    print("Project ID is " + str(pid))
    print("Adapter information: " + str(adapter))
    print("No. of files selected is " + str(len(os.listdir(location))-2))
    print("Data located in: " + str(location))
    a = ("Selected Project is " +
       str(proj) + "\n" +
       "Project ID is " +
       str(pid) + "\n" +
       "Data located in: "+
       str(location))
    answer = tk.messagebox.askyesnocancel("Confirmation", a)    
   
    if answer:
        
        print("################################")
        print("############ Running it all together ###########")
        print("################################")
        location= folderPath.get()
        temp1_path= location + "/" + "temp1.sh"
        os.system("bash " + temp1_path)
        print("################################")
        print("############ Done ###########")
        print("################################")
        
    else:
        rm_cmd=" rm "+ location + "/" + "temp1.sh"
        os.system(rm_cmd) 
        
##################################
######## Refresh basespace #######
##################################

def bsrefresh():
    os.system("basemount basespace/")
    os.system("basemount basespace/")

##########################################
############## PANEL creation ############
##########################################
    
def panel():
    location = folderPath.get()
    file_list=os.listdir(location)
    if 'panel' in file_list:
        os.system("rm -r " + location + "/panel")
 #kit chosen and retrieving adapters 
    libkit=library_kit.get()
    if libkit=="Roche":
        bed_file_loc= "roche_hg19_panel.bed"
    elif libkit=="Illumina":
        bed_file_loc="CEX_illumina_nextera_panel.bed"
    else:
        bed_file_loc="New_agilent_panel.bed"

#project selection and project id retrieval
    proj= project.get()
    if proj=="Somatic DNA":
        proj_dest="Somatic_Patient_Samples"
    elif proj=="Somatic RNA":
        proj_dest="Somatic_Patient_RNA"
    else:
        proj_dest="Germline_Patient_Sample"
    
    samples=[]
    for file in file_list:
        sample= file.split("_")
        samples.append(sample[0])
    samples= pd.unique(samples)
    samples=np.array(samples).tolist()
    if 'temp1.sh' in samples:
        samples.remove('temp1.sh')
    if 'panel' in samples:
        samples.remove('panel')
    if 'panellog.txt' in samples:
        samples.remove('panellog.txt')
    if 'cutadaptlog.txt' in samples:    
        samples.remove('cutadaptlog.txt')
    if 'FQlog.txt' in samples:    
        samples.remove('FQlog.txt')
    if 'MSI' in samples:
        samples.remove('MSI')
    if 'CNV' in samples:
        samples.remove('CNV')
    if 'cutadaptlog' in samples:
        samples.remove('cutadaptlog') 
        
    mkdir="mkdir "+ location+ "/panel"
    os.system(mkdir)
    temp2= location +  "/panel/temp2.sh"
    f1= open(temp2,"x")
    f1.close()
    f1= open(temp2,"w+")
    f1.write("cd "+ location + "/panel" + '\n')
    
    if proj=="Somatic DNA":
        for s in samples:
            f1.write("cp /home/basecare/basespace/Projects/"+ str(proj_dest) + "/AppResults/" + s)
            f1.write("/Files/"+s+ ".hard-filtered.vcf.gz "+ location+ "/panel"+ '\n')
            f1.write('\n')
            f1.write("gzip -dk "+ s+ ".hard-filtered.vcf.gz" + '\n')
            f1.write('\n')
            f1.write("/home/basecare/Programs/./bedtools.static.binary intersect -header -a " + s+".hard-filtered.vcf -b /home/basecare/Patient_samples/bed_files/panel_bed_files/")
            f1.write(str(bed_file_loc)+ " > " + s + ".hard-filtered_panel.vcf")
            f1.write('\n'+ "rm -rf "+ s + ".hard-filtered.vcf")
            f1.write('\n' + "############" +'\n')
        f1.write('\n' +"echo \"######################\"")
        f1.write('\n' +"echo \"######### DONE #########\"")
        f1.write('\n' +"echo \"######################\"")
        f1.close()  
    
    elif proj=="Germline":
        for s in samples:
            f1.write("cp /home/basecare/basespace/Projects/"+ str(proj_dest) + "/AppResults/" + s)
            f1.write("/Files/"+s+ ".hard-filtered.vcf.gz "+ location+ "/panel"+ '\n')
            f1.write('\n')
            f1.write("gzip -dk "+ s+ ".hard-filtered.vcf.gz" + '\n')
            f1.write('\n')
            f1.write('\n' + "############" +'\n')
        f1.write('\n' +"echo \"######################\"")
        f1.write('\n' +"echo \"######### DONE #########\"")
        f1.write('\n' +"echo \"######################\"")
        f1.close()
    
    answer = tk.messagebox.askyesnocancel("Confirmation", "Run panel creation process?")    
   
    if answer:
        print("################################")
        print("############ Creating panel vcfs ###########")
        print("################################")
        location= folderPath.get()
        temp2_path= location + "/panel/" + "temp2.sh >" + location+ "/panel/panellog.txt"
        os.system("bash " + temp2_path)
        print("################################")
        print("############ Panel Created ###########")
        print("################################")
        
    else:
        rm_cmd=" rm "+ location + "/panel/" + "temp2.sh"
        os.system(rm_cmd) 

########################################
############## MSI analysis ############
########################################
        
def msi():
    location = folderPath.get()
    file_list=os.listdir(location)
    if 'MSI' in file_list:
        os.system("rm -r " + location + "/MSI")   
    #project selection and project id retrieval
    proj= project.get()
    if proj=="Somatic DNA":
        proj_dest="Somatic_Patient_Samples"
    elif proj=="Somatic RNA":
        proj_dest="Somatic_Patient_RNA"
    else:
        proj_dest="Germline_Patient_Sample"
    
    samples=[]
    for file in file_list:
        sample= file.split("_")
        samples.append(sample[0])
    samples= pd.unique(samples)
    samples=np.array(samples).tolist()
    if 'temp1.sh' in samples:
        samples.remove('temp1.sh')
    if 'panel' in samples:
        samples.remove('panel')
    if 'panellog.txt' in samples:
        samples.remove('panellog.txt')
    if 'cutadaptlog.txt' in samples:    
        samples.remove('cutadaptlog.txt')
    if 'FQlog.txt' in samples:    
        samples.remove('FQlog.txt')
    if 'MSI' in samples:
        samples.remove('MSI')
    if 'CNV' in samples:
        samples.remove('CNV')
    if 'cutadaptlog' in samples:
        samples.remove('cutadaptlog') 
        
    mkdir="mkdir "+ location+ "/MSI"
    os.system(mkdir)
    msitxt= location +  "/MSI/msi.sh"
    f1= open(msitxt,"x")
    f1.close()
    f1= open(msitxt,"w+")
    f1.write("cd "+ location + "/MSI" + '\n')
    
    for s in samples:
        f1.write('\n' + "/home/basecare/Programs/msisensor2/msisensor2 msi -b 30 -d /home/basecare/Programs/MSI_Mirco_List/micro.list -t ")
        f1.write("/home/basecare/basespace/Projects/" + str(proj_dest) + "/AppResults/" + s)
        f1.write("/Files/"+s+ ".bam ")
        f1.write("-o " + location + "/MSI/" + s + "_msi" + '\n')
    
    f1.write('\n'+"echo \"######################\"")
    f1.write('\n'+"echo \"######### DONE #########\"")
    f1.write('\n'+"echo \"######################\"")
    f1.close()  

    answer = tk.messagebox.askyesnocancel("Confirmation", "Run MSI analysis?")    
   
    if answer:
        print("################################")
        print("############ Running MSI analysis ###########")
        print("################################")
        location= folderPath.get()
        msi_path= location + "/MSI/" + "msi.sh"
        os.system("bash " + msi_path + "> "+ location + "/MSI/msilog.txt")
        print("################################")
        print("############ MSI completed ###########")
        print("################################")
    else:
        rm_cmd=" rm "+ location + "/MSI/" + "msi.sh"
      
########################################
############## CNV analysis ############
########################################
        
def cnv():
    location = folderPath.get()
    file_list=os.listdir(location)
    if 'CNV' in file_list:
        os.system("rm -r " + location + "/CNV")
    
    #kit chosen and retrieving adapters 
    libkit=library_kit.get()
    if libkit=="Roche":
        cnv_loc= "/home/basecare/Patient_samples/bed_files/roche/KAPA HyperExome Design files hg19/KAPA HyperExome_hg19_capture_targets.bed"
    elif libkit=="Illumina":
        cnv_loc="/home/basecare/Patient_samples/bed_files/Illumina_CEX_bed/TruSeq_Exome_TargetedRegions_v1.2.bed"
    else:
        cnv_loc="/home/basecare/Patient_samples/bed_files/v7/SureSelectV7_covered.bed"
    
    mkdir="mkdir "+ location+ "/CNV"
    os.system(mkdir) 
    #project selection and project id retrieval
    proj= project.get()
    if proj=="Somatic DNA":
        proj_dest="Somatic_Patient_Samples"
    elif proj=="Somatic RNA":
        proj_dest="Somatic_Patient_RNA"
    else:
        proj_dest="Germline_Patient_Sample"
    
    samples=[]
    for file in file_list:
        sample= file.split("_")
        samples.append(sample[0])
    samples= pd.unique(samples)
    samples=np.array(samples).tolist()
    
    if 'temp1.sh' in samples:
        samples.remove('temp1.sh')
    if 'panel' in samples:
        samples.remove('panel')
    if 'panellog.txt' in samples:
        samples.remove('panellog.txt')
    if 'cutadaptlog.txt' in samples:    
        samples.remove('cutadaptlog.txt')
    if 'FQlog.txt' in samples:    
        samples.remove('FQlog.txt')
    if 'MSI' in samples:
        samples.remove('MSI')
    if 'CNV' in samples:
        samples.remove('CNV')
    if 'cutadaptlog' in samples:
        samples.remove('cutadaptlog') 
        
    if proj=="Somatic DNA":
        for s in samples:
            os.system("mkdir "+ location+ "/CNV/" + s)
            cnvtxt= location +  "/CNV/" + s + "/" + s+"_cnv.txt"
            f1= open(cnvtxt,"x")
            f1.close()
            f1= open(cnvtxt,"w+")
            f1.write("[general]")
            f1.write('\n'+ "chrLenFile = /home/basecare/Programs/files_for_control_freec/fai_file/my_genome.fa.fai")
            f1.write('\n'+ "chrFiles = /home/basecare/Programs/files_for_control_freec/chromFa/")
            f1.write('\n' + "window = 0" + '\n' +"ploidy = 2" + '\n' + "intercept=1")
            f1.write('\n' + "minMappabilityPerWindow = 0.7" + '\n' + "outputDir = " + location+ "/CNV/" + s)
            f1.write('\n' + "sex=XY" + '\n' + "breakPointType=2" + '\n' + "degree=3")
            f1.write('\n' + "coefficientOfVariation = 0.05" + '\n'+ "breakPointThreshold = 0.6")
            f1.write('\n' + "maxThreads = 30" + '\n' + "sambamba = /usr/bin/sambamba")
            f1.write('\n' + "SambambaThreads = 30" + '\n' + "noisyData = TRUE" + '\n'+ "printNA=FALSE")
            f1.write('\n' + '\n'+ "[sample]" +'\n')
            f1.write('\n' + "mateFile = " + "/home/basecare/basespace/Projects/" + str(proj_dest))
            f1.write("/AppResults/"+ s + "/Files/" + s + ".bam")
            f1.write('\n' + "inputFormat = BAM")
            f1.write('\n' + "mateOrientation = FR")
            f1.write('\n' + '\n' + "[control]" + '\n') 
            f1.write('\n' + "mateFile = /home/basecare/basespace/Projects/Germline_Patient_Sample/AppResults/IN-423-TJWA-B-TRIMMED/Files/IN-423-TJWA-B-TRIMMED.bam")
            f1.write('\n' + "inputFormat = BAM")
            f1.write('\n' + "mateOrientation = FR" + '\n')
            f1.write('\n' + "[BAF]" + '\n')
            f1.write('\n' + "minimalCoveragePerPosition = 5" +'\n')
            f1.write('\n' + "[target]"+ '\n')
            f1.write('\n' + "captureRegions =")
            f1.write(str(cnv_loc)) 
        f1.close()  
        
    elif proj=="Germline":
        for s in samples:
            os.system("mkdir "+ location+ "/CNV/" + s)
            cnvtxt= location +  "/CNV/" + s + "/" + s+"_cnv.txt"
            f1= open(cnvtxt,"x")
            f1.close()
            f1= open(cnvtxt,"w+")
            f1.write("[general]")
            f1.write('\n'+ "chrLenFile = /home/basecare/Programs/files_for_control_freec/fai_file/my_genome.fa.fai")
            f1.write('\n'+ "chrFiles = /home/basecare/Programs/files_for_control_freec/chromFa/")
            f1.write('\n' + "window = 0" + '\n' +"ploidy = 2" + '\n' + "intercept=1")
            f1.write('\n' + "minMappabilityPerWindow = 0.7" + '\n' + "outputDir = " + location+ "/CNV/" + s)
            f1.write('\n' + "sex=XY" + '\n' + "breakPointType=2" + '\n' + "degree=3")
            f1.write('\n' + "coefficientOfVariation = 0.05" + '\n'+ "breakPointThreshold = 0.6")
            f1.write('\n' + "maxThreads = 30" + '\n' + "sambamba = /usr/bin/sambamba")
            f1.write('\n' + "SambambaThreads = 30" + '\n' + "noisyData = TRUE" + '\n'+ "printNA=FALSE")
            f1.write('\n' + '\n'+ "[sample]" +'\n')
            f1.write('\n' + "mateFile = " + "/home/basecare/basespace/Projects/" + str(proj_dest))
            f1.write("/AppResults/"+ s + "/Files/" + s + ".bam")
            f1.write('\n' + "inputFormat = BAM")
            f1.write('\n' + "mateOrientation = FR")
            f1.write('\n' + "[target]"+ '\n')
            f1.write('\n' + "captureRegions =")
            f1.write(str(cnv_loc)) 
        f1.close()
    
        
    cnvrun= location +  "/CNV/run_cnv.sh"
    f2= open(cnvrun,"x")
    f2.close()
    f2= open(cnvrun,"w+")
    f2.write("cd " + location + "/CNV"+ '\n')
    for s in samples:
        f2.write('\n' + "/home/basecare/Programs/FREEC-11.6/src/freec -conf ")
        f2.write(s + "/" + s+"_cnv.txt" + '\n')
        f2.write('\n')
        f2.write("/home/basecare/Programs/./bedtools.static.binary intersect -a " +s +"/" + s + ".bam_CNVs")
        f2.write(" -b /home/basecare/Patient_samples/bed_files/CNV/CNV_36_genes.bed -loj | sort -V | awk -F\"\t\" \'{print $1\"\t\"$2\"\t\"$3\"\t\"$4\"\t\"$5\"\t\"$9}\' | awk -vOFS=\"\t\" \'$1=$1; BEGIN { str=\"Chromosome Start End Predicted_copy_number Type_of_alteration Gene\"; split(str,arr,\" \"); for(i in arr) printf(\"%s\t\", arr[i]);print}\' | awk '$6 != \".\"\' > ")
        f2.write(s + "\"_cnv_output.txt\"" + '\n')
        f2.write('\n'+ "##############################")
    f2.write('\n'+"echo \"######################\"")
    f2.write('\n'+"echo \"######### DONE #########\"")
    f2.write('\n'+"echo \"######################\"")
    f2.close() 
    
    answer = tk.messagebox.askyesnocancel("Confirmation", "Run CNV analysis?")
    
    if answer:
        print("################################")
        print("############ Running CNV analysis ###########")
        print("################################")
        location= folderPath.get()
        cnv_path= location + "/CNV/run_cnv.sh >" + location + "/CNV/cnvlog.txt" 
        os.system("bash " + cnv_path)
        print("################################")
        print("############ CNV analysis completed ###########")
        print("################################")
        
    else:
        rm_cmd=" rm "+ location + "/CNV/run_cnv.sh"

########################################
######## CNV and MSI analysis ##########
########################################
def cnvmsi():
    location = folderPath.get()
    file_list=os.listdir(location)
    if 'MSI' in file_list:
        os.system("rm -r " + location + "/MSI")
    if 'CNV' in file_list:
        os.system("rm -r " + location + "/CNV")
    
    #kit chosen and retrieving adapters 
    libkit=library_kit.get()
    if libkit=="Roche":
        cnv_loc= "/home/basecare/Patient_samples/bed_files/roche/KAPA HyperExome Design files hg19/KAPA HyperExome_hg19_capture_targets.bed"
    elif libkit=="Illumina":
        cnv_loc="/home/basecare/Patient_samples/bed_files/Illumina_CEX_bed/TruSeq_Exome_TargetedRegions_v1.2.bed"
    else:
        cnv_loc="/home/basecare/Patient_samples/bed_files/v7/SureSelectV7_covered.bed"
    
    #CNV part
    mkdir="mkdir "+ location+ "/CNV"
    os.system(mkdir) 
    #project selection and project id retrieval
    proj= project.get()
    if proj=="Somatic DNA":
        proj_dest="Somatic_Patient_Samples"
    elif proj=="Somatic RNA":
        proj_dest="Somatic_Patient_RNA"
    else:
        proj_dest="Germline_Patient_Sample"
    
    samples=[]
    for file in file_list:
        sample= file.split("_")
        samples.append(sample[0])
    samples= pd.unique(samples)
    samples=np.array(samples).tolist()
    
    if 'temp1.sh' in samples:
        samples.remove('temp1.sh')
    if 'panel' in samples:
        samples.remove('panel')
    if 'panellog.txt' in samples:
        samples.remove('panellog.txt')
    if 'cutadaptlog.txt' in samples:    
        samples.remove('cutadaptlog.txt')
    if 'FQlog.txt' in samples:    
        samples.remove('FQlog.txt')
    if 'MSI' in samples:
        samples.remove('MSI')
    if 'CNV' in samples:
        samples.remove('CNV')      
    if 'cutadaptlog' in samples:
        samples.remove('cutadaptlog') 
        
    if proj=="Somatic DNA":
        for s in samples:
            os.system("mkdir "+ location+ "/CNV/" + s)
            cnvtxt= location +  "/CNV/" + s + "/" + s+"_cnv.txt"
            f1= open(cnvtxt,"x")
            f1.close()
            f1= open(cnvtxt,"w+")
            f1.write("[general]")
            f1.write('\n'+ "chrLenFile = /home/basecare/Programs/files_for_control_freec/fai_file/my_genome.fa.fai")
            f1.write('\n'+ "chrFiles = /home/basecare/Programs/files_for_control_freec/chromFa/")
            f1.write('\n' + "window = 0" + '\n' +"ploidy = 2" + '\n' + "intercept=1")
            f1.write('\n' + "minMappabilityPerWindow = 0.7" + '\n' + "outputDir = " + location+ "/CNV/" + s)
            f1.write('\n' + "sex=XY" + '\n' + "breakPointType=2" + '\n' + "degree=3")
            f1.write('\n' + "coefficientOfVariation = 0.05" + '\n'+ "breakPointThreshold = 0.6")
            f1.write('\n' + "maxThreads = 30" + '\n' + "sambamba = /usr/bin/sambamba")
            f1.write('\n' + "SambambaThreads = 30" + '\n' + "noisyData = TRUE" + '\n'+ "printNA=FALSE")
            f1.write('\n' + '\n'+ "[sample]" +'\n')
            f1.write('\n' + "mateFile = " + "/home/basecare/basespace/Projects/" + str(proj_dest))
            f1.write("/AppResults/"+ s + "/Files/" + s + ".bam")
            f1.write('\n' + "inputFormat = BAM")
            f1.write('\n' + "mateOrientation = FR")
            f1.write('\n' + '\n' + "[control]" + '\n') 
            f1.write('\n' + "mateFile = /home/basecare/basespace/Projects/Germline_Patient_Sample/AppResults/IN-423-TJWA-B-TRIMMED/Files/IN-423-TJWA-B-TRIMMED.bam")
            f1.write('\n' + "inputFormat = BAM")
            f1.write('\n' + "mateOrientation = FR" + '\n')
            f1.write('\n' + "[BAF]" + '\n')
            f1.write('\n' + "minimalCoveragePerPosition = 5" +'\n')
            f1.write('\n' + "[target]"+ '\n')
            f1.write('\n' + "captureRegions =")
            f1.write(str(cnv_loc)) 
        f1.close()  
        
    elif proj=="Germline":
        for s in samples:
            os.system("mkdir "+ location+ "/CNV/" + s)
            cnvtxt= location +  "/CNV/" + s + "/" + s+"_cnv.txt"
            f1= open(cnvtxt,"x")
            f1.close()
            f1= open(cnvtxt,"w+")
            f1.write("[general]")
            f1.write('\n'+ "chrLenFile = /home/basecare/Programs/files_for_control_freec/fai_file/my_genome.fa.fai")
            f1.write('\n'+ "chrFiles = /home/basecare/Programs/files_for_control_freec/chromFa/")
            f1.write('\n' + "window = 0" + '\n' +"ploidy = 2" + '\n' + "intercept=1")
            f1.write('\n' + "minMappabilityPerWindow = 0.7" + '\n' + "outputDir = " + location+ "/CNV/" + s)
            f1.write('\n' + "sex=XY" + '\n' + "breakPointType=2" + '\n' + "degree=3")
            f1.write('\n' + "coefficientOfVariation = 0.05" + '\n'+ "breakPointThreshold = 0.6")
            f1.write('\n' + "maxThreads = 30" + '\n' + "sambamba = /usr/bin/sambamba")
            f1.write('\n' + "SambambaThreads = 30" + '\n' + "noisyData = TRUE" + '\n'+ "printNA=FALSE")
            f1.write('\n' + '\n'+ "[sample]" +'\n')
            f1.write('\n' + "mateFile = " + "/home/basecare/basespace/Projects/" + str(proj_dest))
            f1.write("/AppResults/"+ s + "/Files/" + s + ".bam")
            f1.write('\n' + "inputFormat = BAM")
            f1.write('\n' + "mateOrientation = FR")
            f1.write('\n' + "[target]"+ '\n')
            f1.write('\n' + "captureRegions =")
            f1.write(str(cnv_loc)) 
        f1.close()
    
        
    cnvrun= location +  "/CNV/run_cnv.sh"
    f2= open(cnvrun,"x")
    f2.close()
    f2= open(cnvrun,"w+")
    f2.write("cd " + location + "/CNV"+ '\n')
    for s in samples:
        f2.write('\n' + "/home/basecare/Programs/FREEC-11.6/src/freec -conf ")
        f2.write(s + "/" + s+"_cnv.txt" + '\n')
        f2.write('\n')
        f2.write("/home/basecare/Programs/./bedtools.static.binary intersect -a " +s +"/" + s + ".bam_CNVs")
        f2.write(" -b /home/basecare/Patient_samples/bed_files/CNV/CNV_36_genes.bed -loj | sort -V | awk -F\"\t\" \'{print $1\"\t\"$2\"\t\"$3\"\t\"$4\"\t\"$5\"\t\"$9}\' | awk ")
        f2.write("-vOFS=\"\t\" \'$1=$1; BEGIN { str=\"Chromosome Start End Predicted_copy_number Type_of_alteration Gene\"; split(str,arr,\" \"); for(i in arr) printf(\"%s\t\", arr[i]);print}\' | awk '$6 != \".\"\' > ")
        f2.write(s + "\"_cnv_output.txt\"" + '\n')
        f2.write('\n'+ "##############################")
    f2.write('\n'+"echo \"######################\"")
    f2.write('\n'+"echo \"######### DONE #########\"")
    f2.write('\n'+"echo \"######################\"")
    f2.close() 
    
    #MSI part
    
    mkdir="mkdir "+ location+ "/MSI"
    os.system(mkdir)
    msitxt= location +  "/MSI/msi.sh"
    f3= open(msitxt,"x")
    f3.close()
    f3= open(msitxt,"w+")
    f3.write("cd "+ location + "/MSI" + '\n')
    
    for s in samples:
        f3.write('\n' + "/home/basecare/Programs/msisensor2/msisensor2 msi -b 30 -d /home/basecare/Programs/MSI_Mirco_List/micro.list -t ")
        f3.write("/home/basecare/basespace/Projects/" + str(proj_dest) + "/AppResults/" + s)
        f3.write("/Files/"+s+ ".bam ")
        f3.write("-o " + location + "/MSI/" + s + "_msi" + '\n')
    
    f3.write('\n'+"echo \"######################\"")
    f3.write('\n'+"echo \"######### MSI DONE #########\"")
    f3.write('\n'+"echo \"######################\"")
    f3.close()  
    
    
    answer = tk.messagebox.askyesnocancel("Confirmation", "Run CNV and MSI analysis together?")
    
    if answer:
        print("################################")
        print("############ Running CNV and MSI together ###########")
        print("################################")
        location= folderPath.get()   
        msi_path= location + "/MSI/" + "msi.sh"
        os.system("bash " + msi_path + "> "+ location + "/MSI/msilog.txt")
        print("############## MSI analysis completed  ###########")
        cnv_path= location + "/CNV/run_cnv.sh >" + location + "/CNV/cnvlog.txt" 
        os.system("bash " + cnv_path)
        print("############## CNV analysis completed  ###########")
        print("############## MSI and CNV analysis completed  ###########")
    else:
        rm_cmd=" rm "+ location + "/CNV/run_cnv.sh"
        rm_cmd=" rm "+ location + "/MSI/" + "msi.sh"
        
################################################
############# Button ###########################
################################################
        
#browse button
samplelabel= tk.Label(window, text='Choose folder location')
browse_btn=tk.Button(window,text = 'Browse', command = browse, height = 1, width = 18)
samplelabel.config(font=('Nunito Sans',13))

#dropdown for library kits    
kitlabel= tk.Label(window, text= 'Select the library kit')
kitchoosen = ttk.Combobox(window, width = 27, textvariable = library_kit)
kitchoosen['values'] = ('Roche', 'Illumina','Agilent')
kitlabel.config(font=('Nunito Sans',13))

#selecting projects and retrieving project IDs
projectlabel= tk.Label(window, text= 'Select the project')
projectchoosen = ttk.Combobox(window, width = 27, textvariable = project)
projectchoosen['values'] = ('Somatic DNA', 'Somatic RNA','Germline')
projectlabel.config(font=('Nunito Sans',13))

#submit button
sub_btn=tk.Button(window,text = 'Run FQ & CA', command = submit, height = 1, width = 22)

#Dragen Run details
appsessionlabel= tk.Label(window, text='Enter Appsession details')
appsession= tk.Entry(window, width = 27, textvariable=appsession_name)
appsessionlabel.config(font=('Nunito Sans',13))

#Run all at once button
tog_btn=tk.Button(window,text = 'Run FQ, CA and Dragen', command = together, height = 1, width = 22)

#Refresh basespace button
ref_btn=tk.Button(window,text = 'Refresh Basespace', command = bsrefresh, height = 1, width = 22)

#Panel creation button
panel_btn=tk.Button(window,text = 'Panel creation', command = panel, height = 1, width = 22)

#MSI analysis button
msi_btn=tk.Button(window,text = 'MSI analysis', command = msi, height = 1, width = 22)

#CNV analysis button
cnv_btn=tk.Button(window,text = 'CNV analysis', command = cnv, height = 1, width = 22)

#CNV and MSI analysis button
cnvmsi_btn=tk.Button(window,text = 'MSI,CNV&CNV annotation', command = cnvmsi, height = 1, width = 22)

#Quit button
close_btn=tk.Button(window, text="Quit", command=window.destroy, height = 1, width = 22)


################# Positioning ##########################
samplelabel.grid(row=0,column=0,pady=3)
browse_btn.grid(row=0, column=1,pady=3)
kitlabel.grid(row=1, column=0,pady=3)
kitchoosen.grid( row = 1,column = 1,pady=3)
projectlabel.grid(row=2,column=0,pady=3)
projectchoosen.grid(row=2, column=1,pady=3)
appsessionlabel.grid(row=3,column=0,pady=3)
appsession.grid(row=3,column=1,pady=3)
sub_btn.grid(row=4,column=0,pady=3)
tog_btn.grid(row=5,column=0,pady=3)
ref_btn.grid(row=6,column=0,pady=3)
panel_btn.grid(row=7,column=0,pady=3)
msi_btn.grid(row=8,column=0,pady=3)
cnv_btn.grid(row=9,column=0,pady=3)
cnvmsi_btn.grid(row=10,column=0,pady=3)
close_btn.grid(row=11,column=0,pady=3)
 


window.mainloop()        
  

