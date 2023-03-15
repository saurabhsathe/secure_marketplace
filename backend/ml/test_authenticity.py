# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 01:00:53 2022

@author: 16692
"""

import ml.Review_Analysis_Final as model
import pickle
sentences = ["This pillow saved my back. I love the look and feel of this pillow.","This is a soft pillow","This is really great"]



def test_authenticity(sentences):
    
    #preprocess
    temp1=[]
    for sentence in sentences:
        temp1.append(model.preprocess(sentence))
    #stem
    temp2=[]
    for s1 in temp1:
        temp2.append(model.stem_words(s1))
    #lemmetizationt
    temp3=[]
    for s2 in temp2:
        temp3.append(model.lemmatize_words(s2))
    
    cv=None
    tfidf=None
    classifier=None
    
    
    
    pipeline=None
    with open('pipeline.pkl', 'rb') as inp:
        pipeline = pickle.load(inp)
    
    x = list(pipeline.predict(temp3))
    real= x.count("OR")
    fake = x.count("CG")
    
    #return "Real",(real//(real+fake)) if fake<real else "Fake",(fake//(real+fake))
    return ("Real",real//(real+fake)) if fake<real else ("Fake",fake//(real+fake))


#print(test_authenticity("I like it, just wish it had more wide opening. I also love that it's been made"))
#print(test_authenticity("Works as expected for connecting CCTV power supply to cameras."))
#print(test_authenticity(sentences))