#Merging the files and saving inside the merged folder


import pandas as pd
import os
import warnings

collist= pd.read_csv("/home/nishtha/TMB/filtering_script/columns.csv")
dirpath= os.getcwd()
genes= pd.read_csv("/home/nishtha/TMB/filtering_script/som_genes.csv")

folders= os.listdir(dirpath)

os.system("mkdir " + dirpath + "/merged")
warnings.filterwarnings("ignore")

for f in folders:
    num=folders.index(f)
    f_path= dirpath + "/" + f
    files= os.listdir(f_path)
    cancer= [obj for obj in files if 'cancervar.hg19_multianno.txt.cancervar' in obj]
    annovar= [obj for obj in files if '_out.hg19_multianno' in obj]
    vcf= [obj for obj in files if '.tab' in obj]
    print('merging: '+ f)

    #locations of different files
    cancerloc= dirpath + "/" + f + "/" + cancer[0]
    vcfloc= dirpath + "/" + f + "/" + vcf[0]
    annoloc= dirpath + "/" + f + "/" + annovar[0]

    cancercol=collist['cancervar'][collist['cancervar'].notna()]
    cancervar= pd.read_csv(cancerloc, usecols=cancercol, sep='\t')
    
    vcfcol=collist['vcf'][collist['vcf'].notna()]
    vcfcol=[int(i) for i in vcfcol]
    vcf= pd.read_csv(vcfloc, usecols=vcfcol, sep='\t')
    
    annocol=collist['multianno'][collist['multianno'].notna()]
    annovar= pd.read_csv(annoloc,usecols=annocol, sep='\t')

    #rename annovar columns
    annovar=annovar.rename(columns={'Chr':'CHROM', 'Start': 'POS', 'Ref':'REF', 'Alt':'ALT','Gene.knownGene':'Ref.Gene' })
    
    #rename annovar columns
    cancervar=cancervar.rename(columns={'#Chr':'CHROM', 'Start': 'POS', 'Ref':'REF', 'Alt':'ALT','Gene.knownGene':'Ref.Gene' })
    
        
    cancervar['CHROM']=list(map(str, cancervar['CHROM']))
    cancervar['CHROM']='chr' + cancervar['CHROM']
    
    aicdf= pd.merge(annovar,cancervar, on= ['CHROM','POS','End','REF','ALT'])
    merged_df= pd.merge(vcf, aicdf, how='outer', on= ['CHROM','POS'])
       
    merged_df.fillna('.', inplace = True)
    
    #preparing intervar_inhouse columns
    for i in range(34,62):
        merged_df[merged_df.columns[i]]=merged_df.columns[i]+ ":" + merged_df[merged_df.columns[i]]
    
    merged_df['intervar_inhouse']=merged_df[list(merged_df.columns[36:64])].apply(lambda x: ', '.join(x[x.notnull()]), axis = 1)
    
    print(f + " : merged")
        
    #re-arranging the index
    cols=list(merged_df.columns)
    colind= list(collist['reindex'][collist['reindex'].notna()])
    colindex=list( [cols[int(i)] for i in colind] )
                           
    final_df=merged_df[colindex]           
    tot_var=len(final_df)
         
    output_path= dirpath + "/merged/" + f + '_merged_output.csv'        
    final_df.to_csv(output_path, index=False)
    

print("#############################")
print("############ DONE ###########")
print("#############################")
    
    


