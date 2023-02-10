import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
years = []
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"}

for i in range(2012, 2023):
    years.append(i)

df = pd.read_csv('LitQuery_2.csv')

for index, row in df.iterrows():
    
    print(index,"/", df.shape[0], end='\r')
    
    if('pubmed' in row['Link']):
        html = requests.get(row['Link'])
        soup = BeautifulSoup(html.content, 'html.parser')
        try:
            sourceLink = soup.find('a', {'class':'link-item pmc'})['href']
            
            sourceHTML = requests.get(sourceLink, headers=headers)
            sourceSoup = BeautifulSoup(sourceHTML.content, 'html.parser')

            paragraphs = sourceSoup.find_all('p')

            cellValue = []
            for paragraph in paragraphs:
                for sentence in paragraph.text.split('.'):
                    for year in years:
                        year = str (year)
                        for month in months:
                            month = str(month)
                            if(month in sentence.upper() and year in sentence and sentence not in cellValue):
                                # sentence = sentence.replace(year,'\033[1m' + year + '\033[0m')
                                # sentence = sentence.replace(month,'\033[1m' + month + '\033[0m')
                                cellValue.append(sentence)

            # print(cellValue)
        except:
            cellValue = []
            print('Error at this line : ', index)
    
        df.at[index, 'New Research Date'] = str(cellValue)

df.to_csv('output.csv')