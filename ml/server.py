{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "caa2add9",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "[nltk_data] Downloading package wordnet to\n",
      "[nltk_data]     C:\\Users\\16692\\AppData\\Roaming\\nltk_data...\n",
      "[nltk_data]   Package wordnet is already up-to-date!\n"
     ]
    },
    {
     "data": {
      "text/plain": [
       "True"
      ]
     },
     "execution_count": 3,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "import numpy as np\n",
    "import pandas as pd\n",
    "import seaborn as sns\n",
    "import matplotlib.pyplot as plt\n",
    "%matplotlib inline\n",
    "import warnings\n",
    "warnings.filterwarnings('ignore')\n",
    "from nltk.corpus import stopwords\n",
    "from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer\n",
    "from sklearn.metrics import classification_report, confusion_matrix\n",
    "from sklearn.model_selection import train_test_split\n",
    "import string, nltk\n",
    "from nltk import word_tokenize\n",
    "from nltk.stem import PorterStemmer\n",
    "from nltk.stem import WordNetLemmatizer\n",
    "nltk.download('wordnet')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "id": "960000bd",
   "metadata": {},
   "outputs": [],
   "source": [
    "def clean_text(text):\n",
    "    nopunc = [w for w in text if w not in string.punctuation]\n",
    "    nopunc = ''.join(nopunc)\n",
    "    return  ' '.join([word for word in nopunc.split() if word.lower() not in stopwords.words('english')])\n",
    "\n",
    "def preprocess(text):\n",
    "    return ' '.join([word for word in word_tokenize(text) if word not in stopwords.words('english') and not word.isdigit() and word not in string.punctuation])\n",
    "\n",
    "stemmer = PorterStemmer()\n",
    "def stem_words(text):\n",
    "    return ' '.join([stemmer.stem(word) for word in text.split()])\n",
    "\n",
    "\n",
    "lemmatizer = WordNetLemmatizer()\n",
    "def lemmatize_words(text):\n",
    "    return ' '.join([lemmatizer.lemmatize(word) for word in text.split()])\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "id": "dbb2b8d1",
   "metadata": {},
   "outputs": [],
   "source": [
    "def pipeline_step1(txt):\n",
    "    s1 = clean_text(txt)\n",
    "    s2=preprocess(s1)\n",
    "    s3=stem_words(s2)\n",
    "    return lemmatize_words(s3)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 17,
   "id": "6118dbb9",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      " * Serving Flask app \"__main__\" (lazy loading)\n",
      " * Environment: production\n",
      "\u001b[31m   WARNING: This is a development server. Do not use it in a production deployment.\u001b[0m\n",
      "\u001b[2m   Use a production WSGI server instead.\u001b[0m\n",
      " * Debug mode: off\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      " * Running on http://127.0.0.1:5555/ (Press CTRL+C to quit)\n"
     ]
    }
   ],
   "source": [
    "\n",
    "from flask import Flask, jsonify, request\n",
    "\n",
    "from flask_cors import CORS, cross_origin\n",
    "import json\n",
    "# In[3]:\n",
    "app= Flask(__name__)\n",
    "cors = CORS(app)\n",
    "\n",
    "import random\n",
    "@app.route('/predict',methods=[\"POST\"])\n",
    "def predict():\n",
    "    data=json.loads(request.data)\n",
    "    print(data)\n",
    "    rating=data[\"rating\"]\n",
    "    raw_text = data[\"text\"]\n",
    "    preprocessed_text = pipeline_step1(raw_text)\n",
    "    \n",
    "    return random.choice([\"fake\",\"real\"])\n",
    "\n",
    "    \n",
    "#  main thread of execution to start the server\n",
    "if __name__=='__main__':\n",
    "    app.run(host=\"127.0.0.1\",port=5555)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "c44fbcbf",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
