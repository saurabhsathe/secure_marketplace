#export FLASK_APP=app.py
#FLASK_ENV=development
#flask run
from flask import Flask, request, jsonify, json
from flask_cors import CORS, cross_origin
from amazon_comment_scraper import AmazonScraper
from amazon_listings_scraper import scrape_amazon
from ebay_listings_scraper import scrape_ebay
#from amazon_predict_rating import get_listings_with_ratings
from ml.test_authenticity import test_authenticity
import pickle
from nltk.corpus import stopwords
import string
import random

app = Flask(__name__)
app.debug = True
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

pipeline=None

def text_process(review):
    nopunc = [char for char in review if char not in string.punctuation]
    nopunc = ''.join(nopunc)
    return [word for word in nopunc.split() if word.lower() not in stopwords.words('english')]

with open('ml/pipeline.pkl', 'rb') as inp:
        pipeline = pickle.load(inp)

possible_ratings = {'A', 'B', 'C', 'D'}

@app.route("/",methods=['POST'])
@cross_origin()
def home():
    reviews = {'rating': 'A'}

    print(reviews)
    return jsonify(reviews), 200

@app.route("/scrape/<page_no>",methods=['POST'])
@cross_origin()
def scrape_listing(page_no):
    #print(page_no)
    new_scraper = AmazonScraper()
    #print(request.get_json(force=True))
    data = request.get_json(force=True)
    #print(data, page_no)
    reviews = new_scraper.scrapeReviews(data['listing_url'], page_no)
    #print(reviews)
    return jsonify(reviews), 200

#this API will give us the results"
@app.route("/predict",methods=['POST'])
def predict_ratings():

    data = request.get_json(force=True)
    #print(data["reviews"])
    reviews = data["reviews"]
    x,y = test_authenticity(reviews,pipeline)
    return jsonify({"result":x,"percentage":y}), 200

@app.route("/listings/<item_name>",methods=['GET'])
def get_listings_with_ratings(item_name):
    #item_list = []
    item_list = scrape_amazon(item_name, 1)
    #print(item_list)
    #item_list.extend(scrape_amazon(item_name, 2))
    #print(item_list)
    for item in item_list:
        #print(item)
        new_comment_scraper = AmazonScraper()
        reviews = new_comment_scraper.scrapeReviews(item["product_url"], 1)
        # print("*********** REVIEWS *******")
        # print(reviews)
        # print("***************END*******")
        if not reviews or len(reviews) == 0:
            item['safemart_rating'] = ({"result":'-',"percentage":1})
        else:
            x,y = test_authenticity(reviews, pipeline)
            item['safemart_rating'] = ({"result":x,"percentage":y})
            #print(x, y)
    item_list_ebay = scrape_ebay(item_name)
    for item in item_list_ebay:
        rating = random.choice(list(possible_ratings))
        item['safemart_rating'] = ({"result":rating,"percentage":1})

    #print(item_list_ebay)
    item_list.extend(item_list_ebay)

    return jsonify(item_list), 200

if __name__ == '__main__':
    app.run(port=4444)
