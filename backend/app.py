#export FLASK_APP=app.py
#FLASK_ENV=development
#flask run
from flask import Flask, request, jsonify, json, render_template, url_for, session, redirect, flash
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
import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from flask_pymongo import PyMongo
import bcrypt

#uri = "mongodb+srv://admin:admin@safemartcluster.oamjwqk.mongodb.net/?retryWrites=true&w=majority"

app = Flask(__name__, template_folder='../frontend')
app.secret_key = "testing"
client = pymongo.MongoClient("mongodb+srv://admin:admin@safemartcluster.oamjwqk.mongodb.net/?retryWrites=true&w=majority")
db = client.get_database('SafeMart')
records = db.User
app.debug = True
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


#mongo = PyMongo(app)

pipeline=None

def text_process(review):
    nopunc = [char for char in review if char not in string.punctuation]
    nopunc = ''.join(nopunc)
    return [word for word in nopunc.split() if word.lower() not in stopwords.words('english')]

with open('ml/pipeline.pkl', 'rb') as inp:
        pipeline = pickle.load(inp)

possible_ratings = {'A', 'B', 'C', 'D'}
max_list_processing_count = 12

@app.route("/",methods=['POST'])
@cross_origin()
def home_page():
    reviews = {'rating': 'A'}

    print(reviews)
    return jsonify(reviews), 200

@app.route("/signup", methods=['POST', 'GET'])
def signup():
    message = ''
    if "email" in session:
        return redirect(url_for("home"))
    if request.method == "POST":
        user = request.form.get("fullname")
        email = request.form.get("email")
        
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        
        email_found = records.find_one({"email": email})
        if email_found:
            message = 'This email already exists in database'
            return render_template('login.html', message=message)
        if password1 != password2:
            message = 'Passwords should match!'
            return render_template('signup.html', message=message)
        else:
            hashed = bcrypt.hashpw(password2.encode('utf-8'), bcrypt.gensalt())
            user_input = {'name': user, 'email': email, 'password': hashed}
            records.insert_one(user_input)
            
            user_data = records.find_one({"email": email})
            new_email = user_data['email']
   
            session["email"] = new_email
            return redirect(url_for('home'))
    return render_template('signup.html', message=message)

@app.route('/home')
def home():
    if "email" in session:
        email = session["email"]
        return render_template('home-page.html', email=email)
    else:
        return redirect(url_for("login"))
    

@app.route("/login", methods=["POST", "GET"])
def login():
    message = 'Please login to your account'
    if "email" in session:
        print(session["email"])
        return redirect(url_for('home'))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

       
        email_found = records.find_one({"email": email})
        if email_found:
            email_val = email_found['email']
            passwordcheck = email_found['password']
            
            if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                session["email"] = email_val
                return redirect(url_for('home'))
            else:
                if "email" in session:
                    return redirect(url_for('home'))
                message = 'Wrong password'
                return render_template('login.html', message=message)
        else:
            message = 'Email not found'
            return render_template('login.html', message=message)
    print("-------->")
    print("email" in session)
    return render_template('login.html', message=message)

@app.route("/logout", methods=["POST", "GET"])
def logout():
    if "email" in session:
        session.pop("email", None)
        #print(session["email"])
        return render_template("login.html")
    else:
        print(session)
        #print(session["email"] or None)
        return render_template('login.html')

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
    if item_list and len(item_list) > max_list_processing_count:
        item_list = item_list[:max_list_processing_count]
    #print(item_list)
    #item_list.extend(scrape_amazon(item_name, 2))
    #print(item_list)
    for item in item_list:
        new_comment_scraper = AmazonScraper()
        reviews = new_comment_scraper.scrapeReviews(item["product_url"], 1)
        # print("*********** REVIEWS *******")
        # print(reviews)
        # print("***************END*******")
        if not reviews or len(reviews) == 0:
            item['safemart_rating'] = ({"result":'-',"percentage":1})
        else:
            x,y = test_authenticity(reviews, pipeline)
            y = float(y)
            # print("----> ", y)
            a_rating = '-'
            if y >= 90:
                a_rating = 'A'
            elif y >= 80:
                a_rating = 'B'
            elif y >= 70:
                a_rating = 'C'
            else:
                a_rating = 'D'
            item['safemart_rating'] = ({"result":a_rating,"percentage":y})
            #print(x, y)

    #ebay
    item_list_ebay = scrape_ebay(item_name)
    if item_list_ebay and len(item_list_ebay) > max_list_processing_count:
        item_list_ebay = item_list_ebay[:max_list_processing_count]

    for item in item_list_ebay:
        rating = random.choice(list(possible_ratings))
        item['safemart_rating'] = ({"result":rating,"percentage":1})

    #print(item_list_ebay)
    item_list.extend(item_list_ebay)

    return jsonify(item_list), 200

@app.route("/reviews",methods=['POST'])
def get_reviews_with_ratings():

    data = request.get_json(force=True)
    url = data["url"].replace("www.", "")
    new_comment_scraper = AmazonScraper()
    item ={}
    reviews = new_comment_scraper.scrapeReviews(url, 1)
    #print(reviews)
    if len(reviews) == 0:
        item['safemart_rating'] = ({"result":'-',"percentage":1})
    else:
        x,y = test_authenticity(reviews, pipeline)
        item['safemart_rating'] = ({"result":x,"percentage":y})
        #print(x, y)
    return jsonify(item), 200

if __name__ == '__main__':
    app.run(port=4444)
