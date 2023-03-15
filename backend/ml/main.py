# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 01:00:53 2022

@author: 16692
"""

import Review_Analysis_Final as model
import pickle
from Review_Analysis_Final import text_process
sentence = "This pillow saved my back. I love the look and feel of this pillow."



def test_authenticity(sentence):
    #preprocess
    s1 = model.preprocess(sentence)
    #stem
    s2=model.stem_words(s1)
    #lemmetization
    s3 = model.lemmatize_words(s2)
    
    cv=None
    tfidf=None
    classifier=None
    print(s3)
    
    
    
    pipeline=None
    with open('pipeline.pkl', 'rb') as inp:
        pipeline = pickle.load(inp)
    
    x = pipeline.predict([s3])
    return "Fake" if x[0]=="CG" else "Real"

