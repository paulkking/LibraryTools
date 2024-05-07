"""
Alma scraper script; takes input of a folder of HTML files saved from Ex Libris Alma.
HTML files can be downloaded (ctrl+S) from Alma search results.
Returns collection titles and the number of portfolios (ebook/ejournal titles) in each collection in a CSV file.
Useful for QA since portfolio count numbers do not show up in exports; this functionality might be replicable with the Alma API.
"""

from bs4 import BeautifulSoup # Library required for web scraping
import re
import pandas as pd
import os

pages = []
files = os.listdir()

for file in files:
    if file[-4:] == "html":
        with open(file,"rb") as html:
            soup = BeautifulSoup(html, 'html.parser')
            pages.append(soup)

collection_list = [[] for i in range(0,len(files)*10)]
count = 0
for page in pages:
    for i in range (0,20):
        spanID = "SPAN_RECORD_VIEW_results_ROW_ID_" + str(i) + "_LABEL_packageNamepackageName"
        if page.find('span', id=spanID):
            title_tag = page.find('span', id=spanID)
            collection_list[count].append(title_tag.get('title'))
            portfolio_tag = title_tag.find_next('a')
            x = (re.search('\d+',portfolio_tag.get('title'))).group()
            collection_list[count].append(x)
            count +=1

df = pd.DataFrame(collection_list, columns=['Collection Name','Portfolios'])
df = df.dropna()
filename = 'alma_scraper_out.csv'
df.to_csv(filename,index=False)
print(str(len(df)) + " collections found")
print("Portfolio counts exported to " + filename)