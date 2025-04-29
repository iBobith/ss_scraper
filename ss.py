import requests
from bs4 import BeautifulSoup

def get_brand_url(brand):
    brand = brand.lower()
    return f"https://www.ss.lv/en/transport/cars/{brand}/"

def fetch_listings(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept-Language": "en-US,en;q=0.9",
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

    ad_rows = main_table.select('tr[id^=tr_]')

    if not ad_rows:
        print("No listing rows found.")
        return

    for row in ad_rows:
        cols = row.find_all('td')
        if len(cols) < 6:
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
    brand = input("Enter the car brand you want to search for: ").strip().lower()
    url = get_brand_url(brand)
    try:
        html = fetch_listings(url)
        parse_listings(html)
    except requests.HTTPError as e:
        print(f"HTTP error occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
