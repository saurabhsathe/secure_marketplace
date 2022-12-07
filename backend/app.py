from flask import Flask, request, jsonify, json
from amazon_comment_scraper import AmazonScraper
app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Flask!"

@app.route("/scrape/<page_no>",methods=['POST'])
def scrape_listing(page_no):
    print(page_no)
    new_scraper = AmazonScraper()
    print(request.get_json(force=True))
    data = request.get_json(force=True)
    print(data, page_no)
    reviews = new_scraper.scrapeReviews(data['listing_url'], page_no)
    #reviews = "N"
    print(reviews)
    return jsonify(reviews), 200