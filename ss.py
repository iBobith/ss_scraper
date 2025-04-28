import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://www.ss.lv/en/transport/cars/'

def fetch_listings(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text

def parse_listings(html):
    soup = BeautifulSoup(html, 'html.parser')
    
    rows = soup.select('tr[id^=tr_]')

    for row in rows:
        title_element = row.select_one('.msga2-o')
        price_element = row.select_one('.msga2-o.pp6')
        location_element = row.select('td')[-2] if len(row.select('td')) > 1 else None
        date_element = row.select('td')[-1] if len(row.select('td')) > 0 else None

        title = title_element.get_text(strip=True) if title_element else 'N/A'
        price = price_element.get_text(strip=True) if price_element else 'N/A'
        location = location_element.get_text(strip=True) if location_element else 'N/A'
        date = date_element.get_text(strip=True) if date_element else 'N/A'

        print(f"Title: {title}")
        print(f"Price: {price}")
        print(f"Location: {location}")
        print(f"Date: {date}")
        print("-" * 40)

def main():
    html = fetch_listings(BASE_URL)
    parse_listings(html)

if __name__ == "__main__":
    main()
