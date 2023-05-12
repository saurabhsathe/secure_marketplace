
from ml.test_authenticity import test_authenticity
from amazon_comment_scraper import AmazonScraper
from nltk.corpus import stopwords
import string

import pickle

pipeline = None

def text_process(review):
    nopunc = [char for char in review if char not in string.punctuation]
    nopunc = ''.join(nopunc)
    return [word for word in nopunc.split() if word.lower() not in stopwords.words('english')]

with open('ml/pipeline.pkl', 'rb') as inp:
        pipeline = pickle.load(inp)

def get_listings_with_ratings(item_list):
    for item in item_list:
        new_comment_scraper = AmazonScraper()
        reviews = new_comment_scraper.scrapeReviews(item[4], 1)
        x,y = test_authenticity(reviews, pipeline)
        #print("Final result ---------------->")
        #print(x, y)
        item.append({"result":x,"percentage":y})
    return item_list