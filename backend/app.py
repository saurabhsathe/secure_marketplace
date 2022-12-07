from flask import Flask, request, jsonify
from amazon_comment_scraper import AmazonScraper
app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Flask!"

@app.route("/scrape/<page_no>")
def scrape_listing(page_no):
    new_scraper = AmazonScraper()
    reviews = new_scraper.scrapeReviews(request.form['listing_url'], page_no)
    print(reviews)
    return jsonify(reviews), 200