import requests
import time
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

headers = {
    "User-Agent": UserAgent().random,
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": "https://www.amazon.com/"
}

def scrape_amazon(search_term):
    base_url = "https://www.amazon.com/s?k="
    url = base_url + search_term.replace(' ', '+')
    items = []
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        html_content = response.content
        #print("response ", html_content)
        # Parse the HTML content using Beautiful Soup
        soup = BeautifulSoup(html_content, "html.parser")
        results = soup.find_all('div', {'class': 's-result-item', 'data-component-type': 's-search-result'})

        for result in results:
            product_name = result.h2.text

            try:
                rating = result.find('i', {'class': 'a-icon'}).text
                rating_count = result.find_all('span', {'aria-label': True})[1].text
            except AttributeError:
                continue

            try:
                price1 = result.find('span', {'class': 'a-price-whole'}).text
                price2 = result.find('span', {'class': 'a-price-fraction'}).text
                price = price1 + price2
                product_url = 'https://amazon.com' + result.h2.a['href']
                # print(rating_count, product_url)
                items.append([product_name, rating, rating_count, price, product_url])
            except AttributeError:
                continue

        return items
    else:
        print(f"Request failed with status code: {response.status_code}")
    
    # introduce some delay before making the next request
    time.sleep(5)

results = scrape_amazon("iphone")
print(results)