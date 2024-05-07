"""
Run in folder of KBART files. For every KBART, this returns a list of every duplicate title and print/online identifier, and concatenates them into a single CSV.
"""

import os
import pandas as pd
os.getcwd()

kbart_list = os.listdir()

df_list = []
for kbart in kbart_list:
    kbart_df = pd.read_csv(kbart,usecols=['publication_title','print_identifier','online_identifier','title_url'])
    df1=kbart_df.dropna(subset=['publication_title'])[kbart_df.duplicated(subset=['publication_title'],keep=False)]
    df2=kbart_df.dropna(subset=['print_identifier'])[kbart_df.duplicated(subset=['print_identifier'],keep=False)]
    df3=kbart_df.dropna(subset=['online_identifier'])[kbart_df.duplicated(subset=['online_identifier'],keep=False)]
    out_df =pd.concat([df1,df2,df3]).drop_duplicates()
    out_df['filename'] = kbart
    df_list.append(out_df)

results_df = pd.concat(df_list,ignore_index=True)
results_df.to_csv('kbart_duplicates.csv',index=False)