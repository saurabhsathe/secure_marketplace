#export FLASK_APP=app.py
#FLASK_ENV=development
#flask run
from flask import Flask, request, jsonify, json 
from flask_cors import CORS, cross_origin
from amazon_comment_scraper import AmazonScraper
from amazon_listings_scraper import scrape_amazon
from ml.test_authenticity import test_authenticity
import pickle
from nltk.corpus import stopwords
import string

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

@app.route("/listings/<item_name>",methods=['POST'])
def get_listings(item_name):
 
    item_list = scrape_amazon(item_name)
    return jsonify(item_list), 200

if __name__ == '__main__':
    app.run(port=4444)



