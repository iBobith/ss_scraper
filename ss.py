import requests
from bs4 import BeautifulSoup
import time

BASE_URL = "https://www.ss.lv"

def get_brand_url(brand):
    brand = brand.lower()
    return f"{BASE_URL}/en/transport/cars/{brand}/"

def fetch_html(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept-Language": "en-US,en;q=0.9",
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text

def parse_list_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    main_table = soup.find('table', id='page_main')

    if not main_table:
        print("Could not find main listings table.")
        return []

    ad_rows = main_table.select('tr[id^=tr_]')

    links = []
    for row in ad_rows:
        link_tag = row.find('a')
        if link_tag and link_tag.get('href'):
            link = link_tag.get('href')
            full_link = BASE_URL + link
            links.append(full_link)
    return links

def parse_ad_page(html):
    soup = BeautifulSoup(html, 'html.parser')

    title_tag = soup.find('h2')
    if not title_tag:
        title_tag = soup.find('h1')

    if title_tag:
        title = title_tag.get_text(strip=True)
    else:
        title = "No Title Found"

    price_tag = soup.find('td', class_='ads_price')
    if price_tag:
        price = price_tag.get_text(strip=True)
    else:
        price = "No Price Found"

    return title, price

def main():
    brand = input("Enter the car brand you want to search for (e.g., BMW, Audi, Toyota): ").strip().lower()
    list_url = get_brand_url(brand)

    try:
        print(f"Fetching listings for {brand.title()}...")
        list_html = fetch_html(list_url)
        ad_links = parse_list_page(list_html)

        print(f"Found {len(ad_links)} listings.")

        for link in ad_links:
            try:
                ad_html = fetch_html(link)
                title, price = parse_ad_page(ad_html)

                print(f"Car: {title}")
                print(f"Price: {price}")
                print("-" * 40)

                time.sleep(1)
            except Exception as e:
                print(f"Failed to fetch ad {link}: {e}")

    except requests.HTTPError as e:
        print(f"HTTP error occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
