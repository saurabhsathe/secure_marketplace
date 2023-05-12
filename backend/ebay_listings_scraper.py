import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

def scrape_ebay(search_text):
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    url = f'https://www.ebay.com/sch/i.html?_nkw={search_text}'
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    listings = soup.find_all('li', class_='s-item')
    print(len(listings))
    items = []
    for item in listings:
        product_name = item.find('div', class_='s-item__title').text.strip()
        #rating = item.find('div', class_='s-item__reviews').find('div')['aria-label']
        rating=""
        #rating_count = item.find('span', class_='s-item__reviews-count').text.strip()
        rating_count=1
        price = item.find('span', class_='s-item__price').text.strip()
        product_url = item.find('a', class_='s-item__link')['href']
        image_url = item.find('div', class_='s-item__image-wrapper').img['src']
        mktplace = 'Ebay'

        items.append({ "product_name" : product_name,
                               "rating": rating,
                               "rating_count": rating_count,
                               "price": price,
                               "product_url" : product_url,
                               "image_url" : image_url,
                               "mktplace": mktplace})

        #print(f'Product Name: {name}\nRating: {rating}\nRating Count: {rating_count}\nPrice: {price}\nProduct URL: {product_url}\nImage URL: {image_url}\nMarketplace: {mktplace}\n\n')
    if items and len(items) > 0:
        items.pop(0)

    return items

# results = scrape_ebay("table")
# print(results)