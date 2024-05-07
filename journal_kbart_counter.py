"""
    Takes a list of kbarts and returns the filename and number of unique URLs
    Because journal kbarts may have multiple lines for journal holdings, we count only the number of unique Resolver links
"""

import pandas as pd
from os import listdir

def kbart_count(kbart, is_txt=True):
    """
    Input kbart, csv/txt of kbart
    Returns number of unique journals/books in kbart
    """
    if is_txt == True:                  # TXT and CSV files need to be opened differently. By default journals are assumed to be TXT
        df_kbart = pd.read_csv(kbart, 
            usecols=['title_url'], 
            delimiter="	",
            skiprows = 1
            )
        
    else:
        df_kbart = pd.read_csv(kbart, 
            usecols=['title_url']
            )
    
    df_kbart = df_kbart.drop_duplicates(subset=['title_url'])   # Remove duplicate URLs (ie. multiple holdings lines) from kbart
    df_kbart = df_kbart.fillna(0)
    return len(df_kbart) # returns number of unique journal titles (resolver links) in KBART

def journals_track(output_dir, out_delim=','):
    file_names = listdir()
    df_output = pd.DataFrame(columns=['filename','ISSN_count'])
    index_df = 0
    for name in file_names:
        if name[:3] =="sp_" and name[-4:] == ".txt":
            count = kbart_count(name, is_txt = True)
            df_output.loc[index_df] = [
                    name,
                    count
                    ]
            index_df += 1
    df_output.to_csv(output_dir, index=False, sep=out_delim)
    print(str(index_df) + " journal KBARTs processed")
    print("Title counts outputted to " + output_dir)
    return None