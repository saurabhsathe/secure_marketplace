from flask import Flask, request, jsonify, json 
from flask_cors import CORS, cross_origin
from amazon_comment_scraper import AmazonScraper
from test_authenticity import test_authenticity
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
from ml.Review_Analysis_Final import text_process

@app.route("/",methods=['POST'])
@cross_origin()
def home():
    reviews = {'rating': 'A'}
    
    print(reviews)
    return jsonify(reviews), 200

@app.route("/scrape/<page_no>",methods=['POST'])
def scrape_listing(page_no):
    print(page_no)
    new_scraper = AmazonScraper()
    print(request.get_json(force=True))
    data = request.get_json(force=True)
    print(data, page_no)
    reviews = new_scraper.scrapeReviews(data['listing_url'], page_no)
    reviews = "N"
    print(reviews)
    return jsonify(reviews), 200

#this API will give us the results"
@app.route("/predict",methods=['POST'])
def predict_ratings():
 
    data = request.get_json(force=True)
    print(data["reviews"])
    reviews = data["reviews"]
    x,y = test_authenticity(reviews)
    return jsonify({"result":x,"percentage":y}), 200




