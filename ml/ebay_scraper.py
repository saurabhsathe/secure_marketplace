from bs4 import BeautifulSoup
import requests, json, lxml, os
from serpapi import GoogleSearch

from bs4 import BeautifulSoup
import requests, json, lxml

headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}
import pandas as pd

def get_organic_results(query):
    html = requests.get('https://www.ebay.com/sch/i.html?_nkw={}'.format(query), headers=headers).text
    soup = BeautifulSoup(html, 'lxml')

    data = []

    for item in soup.select('.s-item__wrapper.clearfix'):
        title = item.select_one('.s-item__title').text
        link = item.select_one('.s-item__link')['href']

        try:
            condition = item.select_one('.SECONDARY_INFO').text
        except:
            condition = None

        try:
            shipping = item.select_one('.s-item__logisticsCost').text
        except:
            shipping = None

        try:
            location = item.select_one('.s-item__itemLocation').text
        except:
            location = None

        try:
            watchers_sold = item.select_one('.NEGATIVE').text
        except:
            watchers_sold = None

        if item.select_one('.s-item__etrs-badge-seller') is not None:
            top_rated = True
        else:
            top_rated = False

        try:
            bid_count = item.select_one('.s-item__bidCount').text
        except:
            bid_count = None

        try:
            bid_time_left = item.select_one('.s-item__time-left').text
        except:
            bid_time_left = None

        try:
            reviews = item.select_one('.s-item__reviews-count span').text.split(' ')[0]
        except:
            reviews = None

        try:
            exctention_buy_now = item.select_one('.s-item__purchase-options-with-icon').text
        except:
            exctention_buy_now = None

        try:
            price = item.select_one('.s-item__price').text
        except:
            price = None

        data.append({
            'item': {'title': title, 'link': link, 'price': price},
            'condition': condition,
            'top_rated': top_rated,
            'reviews': reviews,
            'watchers_or_sold': watchers_sold,
            'buy_now_extention': exctention_buy_now,
            'delivery': {'shipping': shipping, 'location': location},
            'bids': {'count': bid_count, 'time_left': bid_time_left},
        })

    #print(json.dumps(data, indent = 2, ensure_ascii = False))
    df=pd.DataFrame(data)
    df.to_csv("data.csv")
    print("data retrieved successfully")

mydata=input("please enter your item of interest")

get_organic_results(mydata)

# part of the output:
'''
[
  {
    "item": {
      "title": "Minecraft Overworld Diamond Action Figure Toy Steve Enderman Creeper Collection",
      "link": "https://www.ebay.com/itm/224433499750?_trkparms=ispr%3D1&hash=item3441476e66:g:EaAAAOSw20xgf7dY&amdata=enc%3AAQAGAAACoPYe5NmHp%252B2JMhMi7yxGiTJkPrKr5t53CooMSQt2orsSvtkx670Z0mbyfWqmxLFLYRANDiPOYlNvip6TXpLHigEvqpL5r0bHCZUi1RNW0AmKOb%252FIUIc%252FFDzouRq6XEAsFgkUTV%252BjgofDCIitmj01UxQo9UMhLDq7opbN31c0RL%252Bv07UXSMfkwzYWkzLu1XwuH7LWKtqdxneY%252FEurfMj466vHliEzbyo96BcRaAk7Ho7FLNvIjMxvNUPLzS8QBggEMASGqfLydtgQwyvdqxf2Zga4D%252F9615pGPPBKVkuunMdDwDKBYTMujyu%252Fxo7wlc93IfWRgnww4SRLtHemWiwCmImsWbAqScgH7zXbMD62Vup%252F8HtJPyYsfspo2aagZ6CFOSSmXaIkVRylV1UjrD2TCjuDKGG9tKfcYn3%252BKNFigCjw0FQWkKu7hCigpsWHZYzQUg2rz35j%252BXNIkcawoYJ7HTDYV4uZY95BzLzZ0GWYfqEOWj7TVBOGFdzocR1Ic98dMcHYk4YPPi14Qo0R2CQdMmwmfKxnH2ROIkCYtrKu8rQlPmiDqMRYWVz08g9o1KlD7sJGKL2unIjAFS7AwWxZCpTl0EHiFJo03tGWuS6q5VD%252F88EVpwvvTVFb4zpDeaLUD3q2y6QXbzc3lPJAh2HydbilTqpbhnaAkiLNadxmdxB0DKD7skTcHnq8Vq%252FixA1dqtTCF%252BqnFaNxCnruZMBBxXvUXxPUkxVAGOE%252BByPPGU9uYLKuoSvBVyvUwUwrRRXOIi%252F325u374W%252F%252FwhgKUCHEQ1aK4Z%252BVHCiSAMECrONLheth4CMqO9%252BbJf7Hk3wcDuD1JG5utkYst2C82PJwZDRgKGueCimYYsOL60YBSrz95uE9nd9JF9ZDWwnF42iavQpOw%253D%253D%7Campid%3APL_CLK%7Cclp%3A2334524",
      "price": "$6.70 to $37.65"
    },
    "condition": "Brand New",
    "top_rated": false,
    "reviews": null,
    "watchers_or_sold": "5+ watchers",
    "buy_now_extention": "Buy It Now",
    "delivery": {
      "shipping": "Free International Shipping",
      "location": "from China"
    },
    "bids": {
      "count": null,
      "time_left": null
    }
  }
]
'''