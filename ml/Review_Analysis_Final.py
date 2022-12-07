#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import warnings
warnings.filterwarnings('ignore')
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


df = pd.read_csv('fake reviews dataset.csv')
df.head()


# In[3]:


df.dropna(inplace=True)


# In[8]:


def clean_text(text):
    nopunc = [w for w in text if w not in string.punctuation]
    nopunc = ''.join(nopunc)
    return  ' '.join([word for word in nopunc.split() if word.lower() not in stopwords.words('english')])


# In[9]:

"""
df['text_'][0], clean_text(df['text_'][0])


# In[10]:


df['text_'] = df['text_'].astype(str)


# In[11]:

"""
def preprocess(text):
    return ' '.join([word for word in word_tokenize(text) if word not in stopwords.words('english') and not word.isdigit() and word not in string.punctuation])


# In[12]:
"""

df['text_'][:10000] = df['text_'][:10000].apply(preprocess)


# In[13]:


df['text_'][10001:20000] = df['text_'][10001:20000].apply(preprocess)


# In[14]:


df['text_'][20001:30000] = df['text_'][20001:30000].apply(preprocess)


# In[15]:


df['text_'][30001:40000] = df['text_'][30001:40000].apply(preprocess)


# In[16]:


df['text_'][40001:40432] = df['text_'][40001:40432].apply(preprocess)


# In[17]:


df['text_'] = df['text_'].str.lower()


# In[18]:

"""
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