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

    main_table = soup.find('table', id='page_main')

    if not main_table:
        print("Could not find main listings table.")
        return

    rows = main_table.find_all('tr', id=lambda x: x and x.startswith('tr_'))

    if not rows:
        print("No ad rows found.")
        return

    for row in rows:
        cols = row.find_all('td')

        if len(cols) < 5:
            continue 
        
        title = cols[2].get_text(strip=True)
        location = cols[3].get_text(strip=True)
        date = cols[4].get_text(strip=True)
        price = cols[5].get_text(strip=True)

        print(f"Title: {title}")
        print(f"Location: {location}")
        print(f"Date: {date}")
        print(f"Price: {price}")
        print("-" * 40)

def main():
    html = fetch_listings(BASE_URL)
    parse_listings(html)

if __name__ == "__main__":
    main()
