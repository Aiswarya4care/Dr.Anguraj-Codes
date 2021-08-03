import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
  
window=tk.Tk()
 
# setting the windows size
window.geometry("600x400")
  
# declaring string variab nle
library_kit=tk.StringVar()
location_name=tk.StringVar()
project= tk.StringVar()

# defining a function that will
def submit():
#retrieving sample name
    location= location_name.get()
#kit chosen and retrieving adapters 
    libkit=library_kit.get()
    if libkit=="Roche":
        adapter="adapter for roche"
    elif libkit=="Illumina":
        adapter="adapter for illumina"
    else:
        adapter="adapter for agilent"

#project selection and project id retrieval
    proj= project.get()
    if proj=="Somatic DNA":
        pid="175429254"
    elif proj=="Somatic RNA":
        pid="somr123"
    else:
        pid="germ123"

    print(adapter)
    print(location)
    print(pid)
    l1="perl /home/basecare/Programs/fastqc_v0.11.9/FastQC/fastqc *_R1.fastq.gz *_R2.fastq.gz"
    l2="for i in *_R1.fastq.gz"
    l3="do"
    l4="   SAMPLE=$(echo ${i} | sed \"s/_R1\.fastq\.gz//\") "
    l5="   echo ${SAMPLE}_R1.fastq.gz ${SAMPLE}_R2.fastq.gz"
    l6="   cutadapt -j 20 -m 35 -a AGATCGGAAGAGC -A AGATCGGAAGAGC -o ${SAMPLE}_S1_L001_R1_001.fastq.gz -p ${SAMPLE}_S1_L001_R2_001.fastq.gz ${SAMPLE}_R1.fastq.gz ${SAMPLE}_R2.fastq.gz"
    l7="done"
    l8="bs upload dataset --project="
    l9="perl /home/basecare/Programs/fastqc_v0.11.9/FastQC/fastqc *R1_001.fastq.gz *R2_001.fastq.gz"
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
    f.write('\n' + l7)
    f.write('\n'+ l8 + str(pid) + " *R1_001.fastq.gz *R2_001.fastq.gz")
    f.write('\n' + l9)
    f.close()
    
#entering location
samplelabel= tk.Label(window, text='Enter folder location')
location= tk.Entry(window, textvariable=location_name)


    
#dropdown for library kits    
kitlabel= tk.Label(window, text= 'Select the library kit')
kitchoosen = ttk.Combobox(window, width = 27, textvariable = library_kit)
kitchoosen['values'] = ('Roche', 'Illumina','Agilent')

#selecting projects and retrieving project IDs
projectlabel= tk.Label(window, text= 'Select the project')
projectchoosen = ttk.Combobox(window, width = 27, textvariable = project)
projectchoosen['values'] = ('Somatic DNA', 'Somatic RNA','Germline')

#submit button

sub_btn=tk.Button(window,text = 'Submit', command = submit)


#Positioning
samplelabel.grid(row=0,column=0)
location.grid(row=0, column=1)
kitlabel.grid(row=1, column=0)
kitchoosen.grid( row = 1,column = 1)
projectlabel.grid(row=2,column=0)
projectchoosen.grid(row=2, column=1)
sub_btn.grid(row=3,column=0)

window.mainloop()
