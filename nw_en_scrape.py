import nltk
nltk.download('punkt')
import newspaper
import pandas as pd
import csv
from newspaper import Article
from newspaper import fulltext
import requests
from bs4 import BeautifulSoup
from pprint import pprint
import pandas as pd
import csv
from random import randint
import os
import time
from time import sleep

df = pd.read_csv (r'/XXXXXXX/Covid_Master.csv', encoding = "ISO-8859-1", engine='python')
list_of_urls = df['link'].tolist()

rows = []
for url in list_of_urls:
    try:
        a = Article(url="%s" % (url), language='en')
        a.download()
        a.parse()
         
        author = a.authors
        date = a.publish_date
        text = a.text
        title = a.title
        keywords = a.keywords
        
        
        row = {'url':url,
               'author':author,
               'data':date,
               'text':text,
               'title': title, 
               'keywords':keywords}
        
        rows.append(row)
    except Exception as e:
        print(e)
        row = {'url':url,
        'author':'N/A',
        'date':'N/A',
        'text':'N/A',
        'title': 'N/A',
        'keywords': 'N/A'}
        
        rows.append(row)

df_v1 = pd.DataFrame(rows)
df_v1.to_csv('my_scraped_articles_master.csv')

dfmaster = dfmain.merge(df_v1, left_on='url', right_on='url')
dfmaster.to_csv('my_scraped_articles_master_v1.csv')

df_na = df_v1.loc[df_v1['text'] == 'N/A']

list_of_urls = df_na['url'].tolist()

rows = []
for link in list_of_urls:
    try:
        sleep(randint(3, 7))
        r = requests.get(link)
        soup = BeautifulSoup(r.content, "html.parser")
        text = soup.find_all(text=True)
        
        output = ''
        blacklist = [
            '[document]',
            'noscript',
            'header',
            'html',
            'meta',
            'head', 
            'input',
            'script',
    # there may be more elements you don't want, such as "style", etc.
        ]
        for t in text:
            if t.parent.name not in blacklist:
                output += '{} '.format(t)
        row = {'link':link,
               'soup':soup,
               'text':text,
              'output':output}
        
        rows.append(row)
    except Exception as e:
        row = {'link':link,
        'soup':'N/A',
        'text':'N/A',
        'output':'N/A'}
        
        rows.append(row)
        
df_na_scraped = pd.DataFrame(rows)

##save as backup
df_na_scraped.to_csv('my_scraped_articles.csv')

dfmaster = dfmain.merge(df_na_scraped, left_on='url', right_on='link')
dfmaster.to_csv('my_scraped_articles_master_FV.csv')