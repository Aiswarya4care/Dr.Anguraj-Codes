#merging and filtering
#filtering parameters re-arrangement
# included MQ and allele frequency
#filtering out heterozygous

import pandas as pd
import os
import warnings

dirpath= os.getcwd()

collist= pd.read_csv("/home/nishtha/TMB/filtering_script/columns.csv")
hetero= pd.read_csv("/home/ash/Downloads/TMB_filtering/Refined_Cohort_Heterozygotes.csv", sep='\t')

folders= os.listdir(dirpath)

os.system("mkdir " + dirpath + "/merged")
os.system("mkdir " + dirpath + "/filtered")
warnings.filterwarnings("ignore")

filtered_df= pd.DataFrame(columns=['samplename','total_var','after allele freq', 'after mq', 'after dp', 'after exonic', 'after synony', 'after pop_freq', 'after allege freq2', 'after cdfd'])

for f in folders:
    num=folders.index(f)
    f_path= dirpath + "/" + f
    files= os.listdir(f_path)
    cancer= [obj for obj in files if 'cancervar.hg19_multianno.txt.cancervar' in obj]
    annovar= [obj for obj in files if '_out.hg19_multianno' in obj]
    vcf= [obj for obj in files if '.tab' in obj]
    print(f)

    #locations of different files
    cancerloc= dirpath + "/" + f + "/" + cancer[0]
    vcfloc= dirpath + "/" + f + "/" + vcf[0]
    annoloc= dirpath + "/" + f + "/" + annovar[0]

    cancercol=collist['cancervar'][collist['cancervar'].notna()]
    cancervar= pd.read_csv(cancerloc, usecols=cancercol, sep='\t')
    
    vcfcol=collist['vcf_wo_art'][collist['vcf_wo_art'].notna()]
    vcfcol=[int(i) for i in vcfcol]
    vcf= pd.read_csv(vcfloc, usecols=vcfcol, sep='\t')
    
    annocol=collist['multianno'][collist['multianno'].notna()]
    annovar= pd.read_csv(annoloc,usecols=annocol, sep='\t')
    
    # modifying vcf position values
    
    for i in range(len(vcf)):
        if len(vcf['REF'][i])>len(vcf['ALT'][i]):
            vcf['POS'][i]=vcf['POS'][i]+1
            
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
    for i in range(29,56):
        merged_df[merged_df.columns[i]]=merged_df.columns[i]+ ":" + merged_df[merged_df.columns[i]]
    
    merged_df['intervar_inhouse']=merged_df[list(merged_df.columns[36:64])].apply(lambda x: ', '.join(x[x.notnull()]), axis = 1)
    
    print(f + " : merged")
        
    #re-arranging the index
    cols=list(merged_df.columns)
    colind= list(collist['reindex_wo_art'][collist['reindex_wo_art'].notna()])
    colindex=list( [cols[int(i)] for i in colind] )
                           
    final_df=merged_df[colindex]           
    tot_var=len(final_df)
         
    output_path= dirpath + "/merged/" + f + '_merged_output.csv'        
    final_df.to_csv(output_path, index=False)
    
    ####################################
    ############## Filtration ##########
    
    df= final_df
    
    ######### filtering allele frequency ###############
    
    allele_freq=list(df.columns[df.columns.str.contains(':AF')])[0]
    df[allele_freq]=df[allele_freq].replace('.',100).fillna(100) 
    df[allele_freq]=  df[allele_freq].astype(float)
    df=df[df[allele_freq]>=0.05]
        
    afallele=len(df)
    
    
    ######## filtering MQ ###################
    mq=list(df.columns[df.columns.str.contains(':MQ')])[0]
    df[mq]=df[mq].replace('.',100).fillna(100) 
    df[mq]=  df[mq].astype(float)
    df=df[df[mq]>=10]
       
    afmq=len(df)
    
    ########## Filtering DP
    dp=list( df.columns[df.columns.str.contains("DP")])[0]
    df[dp]=df[dp].replace('.',100).fillna(100) 
    df[dp]=  df[dp].astype(float)
    df=df[df[dp]>=5]
    
    afdp=len(df)
    
    ####### filtering Func.knownGene
   
    df= df[df['Func.knownGene'].str.contains('exonic|splicing', case=False, regex=True)]
    df= df[df['Func.knownGene'].str.contains('RNA')==False]
    afknowngene= len(df)   
    
    ##### filtering synonymous
    df= df[df['ExonicFunc.knownGene']!='synonymous SNV']
    df= df[df['ExonicFunc.knownGene']!='.']
    afsynony= len(df)  
    
    #####filtering pop freq
        
    popfreqs=['esp6500siv2_all','ExAC_ALL','ExAC_SAS','AF','AF_sas','1000g2015aug_all','1000g2015aug_SAS']
        
    print(f + " filtering in progress..")
    for p in popfreqs:
        df[p]=df[p].replace('.',0).fillna(0) 
        df[p]=df[p].replace('.',100).fillna(100) 
        df[p]=  df[p].astype(float)
        df=df[df[p]< 0.01]
        
    afpop=len(df)
        
    ########## Filtering allele freq 0.44 & 0.55
    df=df[list(df[allele_freq]>=0.55) or list(df[allele_freq]<=0.44)]
    
    af_alfq=len(df)
     
                
    print(f + " :filtered")
    
    ############### Filtering CDFD homozygous ############
    
    hetero=hetero[hetero['Heterozygotes']!=0]
    hetero=hetero.rename(columns={'#Chr':'CHROM', 'Start':'POS', 'Ref':'REF_y', 'Alt':'ALT_y'})
    hetero['CHROM'] = ['chr' + str(hetero['CHROM'].iloc[row]) for row in range(len(hetero))]
    
    df=df.merge(hetero, how = 'outer' ,indicator=True).loc[lambda x : x['_merge']=='left_only']

    afcdfd= len(df)
    
    ###################################
    ### making filtered csv
    to_append= [f,tot_var,afknowngene,afsynony,afallele, afmq, afdp,afpop,af_alfq,afcdfd]
    dflen=len(filtered_df)
    filtered_df.loc[dflen]=to_append
    print(to_append)  
    
    output_path= dirpath + "/filtered/" + f + '_filtered_output.csv'        
    df.to_csv(output_path, index=False)
    
    print( "###" + str(num+1) + " out of " + str(len(folders)) + " files done")
            
filtered_df.to_csv(dirpath+"/"+"filtered.csv")    

print("#############################")
print("############ DONE ###########")
print("#############################")
    
    


