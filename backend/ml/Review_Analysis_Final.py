#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import warnings
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.model_selection import train_test_split
import string, nltk
from nltk import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
nltk.download('wordnet')


# In[2]:




# In[8]:


def clean_text(text):
    nopunc = [w for w in text if w not in string.punctuation]
    nopunc = ''.join(nopunc)
    return  ' '.join([word for word in nopunc.split() if word.lower() not in stopwords.words('english')])


# In[9]:


def preprocess(text):
    # print("------------->")
    # print(text)
    # print("------------->")
    return ' '.join([word for word in word_tokenize(text.comment) if word not in stopwords.words('english') and not word.isdigit() and word not in string.punctuation])


stemmer = PorterStemmer()
def stem_words(text):
    return ' '.join([stemmer.stem(word) for word in text.split()])
"""
df['text_'] = df['text_'].apply(lambda x: stem_words(x))
# In[19]:
"""
lemmatizer = WordNetLemmatizer()
def lemmatize_words(text):
    return ' '.join([lemmatizer.lemmatize(word) for word in text.split()])
"""
df["text_"] = df["text_"].apply(lambda text: lemmatize_words(text))
"""
# In[20]:


#df.head()


# In[21]:


#df.dropna(inplace=True)


# In[22]:


#df['length'] = df['text_'].apply(len)


# In[23]:


def text_process(review):
    nopunc = [char for char in review if char not in string.punctuation]
    nopunc = ''.join(nopunc)
    return [word for word in nopunc.split() if word.lower() not in stopwords.words('english')]


# In[24]:


"""bow_transformer = CountVectorizer(analyzer=text_process)
bow_transformer.fit(df['text_'])
print("Total Vocabulary:",len(bow_transformer.vocabulary_))
# In[32]:
import pickle
with open('bow.pkl', 'wb') as outp:
    pickle.dump(bow_transformer, outp, pickle.HIGHEST_PROTOCOL)
# In[26]:
bow_reviews = bow_transformer.transform(df['text_'])
# In[29]:
pd.DataFrame(bow_reviews).to_csv("bagofwords.csv")
# In[30]:
print("Shape of Bag of Words Transformer for the entire reviews corpus:",bow_reviews.shape)
print("Amount of non zero values in the bag of words model:",bow_reviews.nnz)
# In[33]:
tfidf_transformer = TfidfTransformer()
tfidf_transformer.fit(bow_reviews)
with open('tfidf.pkl', 'wb') as outpidf:
    pickle.dump(tfidf_transformer, outpidf, pickle.HIGHEST_PROTOCOL)
# In[34]:
tfidf_reviews = tfidf_transformer.transform(bow_reviews)
print("Shape:",tfidf_reviews.shape)
print("No. of Dimensions:",tfidf_reviews.ndim)
# In[35]:
review_train, review_test, label_train, label_test = train_test_split(df['text_'],df['label'],test_size=0.35)
# In[38]:
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
pipeline = Pipeline([
    ('bow',CountVectorizer(analyzer=text_process)),
    ('tfidf',TfidfTransformer()),
    ('classifier',RandomForestClassifier())
])
# In[39]:
pipeline.fit(review_train,label_train)
# In[40]:
rfc_pred = pipeline.predict(review_test)
# In[42]:
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
print('Classification Report:',classification_report(label_test,rfc_pred))
print('Confusion Matrix:',confusion_matrix(label_test,rfc_pred))
print('Accuracy Score:',accuracy_score(label_test,rfc_pred))
print('Model Prediction Accuracy:',str(np.round(accuracy_score(label_test,rfc_pred)*100,2)) + '%')
# In[43]:
import pickle
with open('pipeline.pkl', 'wb') as out_pipeline:
    pickle.dump(pipeline, out_pipeline, pickle.HIGHEST_PROTOCOL)
# In[ ]:
"""