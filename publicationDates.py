import pandas as pd
import requests
from bs4 import BeautifulSoup


df = pd.read_csv('LitQuery_2.csv')

for index, row in df.iterrows():
    
    print(index,"/", df.shape[0], end='\r')
    
    if('pubmed' in row['Link']):
        html = requests.get(row['Link'])
        soup = BeautifulSoup(html.content, 'html.parser')
        try:
            date = soup.find('span', {'class':'cit'}).text.split(';')[0]
        except:
            print('Error at this line : ', index)
            date = ''
    
    else :
        date = ''
    
    df.at[index, 'New Publication Date'] = date

df.to_csv('output.csv')