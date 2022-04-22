from bertopic import BERTopic
import pandas as pd
import csv
import re
import string
import datetime
import scipy
import numpy
from scipy import sparse
import sys   
import unicodedata
import nltk 
import numpy as np  
import hdbscan
from scipy.sparse import csr_matrix, csc_matrix 

from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-mpnet-base-v2')

nwdata = pd.read_csv(r'/XXXXXX/NW_USA_Python.csv', encoding = "ISO-8859-1", engine='python')
nwdata.dropna(subset=['text'])
nwdata = nwdata[pd.notnull(nwdata['date'])]
nwdata['date'] = pd.to_datetime(nwdata["date"], utc=True)
#nwdata.info()
#nwdata.head()

stop_words = pd.read_csv(r'/XXXXXX/stop_words.csv', encoding = "ISO-8859-1", engine='python')
stop_words = stop_words.text.to_list()

def text_clean(x):

    ### Light
    x = x.lower() # lowercase everything
    x = x.encode('ascii', 'ignore').decode()  # remove unicode characters
    x = re.sub(r'https*\S+', ' ', x) # remove links
    x = re.sub(r'http*\S+', ' ', x)
    # cleaning up text
    x = re.sub(r'\'\w+', '', x) 
    x = re.sub(r'\w*\d+\w*', '', x)
    x = re.sub(r'\s{2,}', ' ', x)
    x = re.sub(r'\s[^\w\s]\s', '', x)
    
    ### Heavy
    x = ' '.join([word for word in x.split(' ') if word not in stop_words])
    x = re.sub(r'@\S', '', x)
    x = re.sub(r'#\S+', ' ', x)
    x = re.sub('[%s]' % re.escape(string.punctuation), ' ', x)
    # remove single letters and numbers surrounded by space
    x = re.sub(r'\s[a-z]\s|\s[0-9]\s', ' ', x)

    return x

nwdata['cleaned_text'] = nwdata.text.apply(text_clean)

timestamps = nwdata.date.to_list()
nwtext = nwdata.cleaned_text.to_list()

start_time = time.time()
topic_model = BERTopic(embedding_model=model, nr_topics="auto", top_n_words=30, calculate_probabilities = True).fit(nwtext)
print("--- %s seconds ---" % (time.time() - start_time))

docs = topic_model.get_representative_docs()
freq = topic_model.get_topic_info()
freq.to_csv("nw_usa_bert_freq_4422.csv")

topic_model.save("modelbert_4422") 

start_time = time.time()
topics, probs = topic_model.fit_transform(nwtext)
topics_over_time = topic_model.topics_over_time(nwtext, topics, timestamps, nr_bins=20)
topics_over_time.to_csv("nw_usa_bert_topics_overtime_4422.csv")
print("--- %s seconds ---" % (time.time() - start_time))

start_time = time.time()
topics= topic_model._map_predictions(topic_model.hdbscan_model.labels_)
probs = hdbscan.all_points_membership_vectors(topic_model.hdbscan_model)
probs = topic_model._map_probabilities(probs, original_topics=True)

df_probs = pd.DataFrame(probs)
df_probs.to_csv("nw_usa_bert_topics_probs_41522.csv")
print("--- %s seconds ---" % (time.time() - start_time))
