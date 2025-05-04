import requests
from bs4 import BeautifulSoup
import csv
import os

BASE_URL = "https://www.ss.lv"

def get_brand_url(brand, page=1):
    brand = brand.lower()
    if page == 1:
        return f"{BASE_URL}/en/transport/cars/{brand}/"
    else:
        return f"{BASE_URL}/en/transport/cars/{brand}/page{page}.html"

def fetch_html(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept-Language": "en-US,en;q=0.9",
    }
    response = requests.get(url, headers=headers, timeout=10)
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

def clean_car_name(name):
    # Remove unnecessary parts from the car name
    parts = name.split('/')
    parts = [part.strip() for part in parts if part.strip() and part.strip().lower() not in ['cars', 'buy', 'sell', 'change']]
    cleaned_name = ' '.join(parts)
    return cleaned_name

def parse_ad_page(html):
    soup = BeautifulSoup(html, 'html.parser')

    # Get car name
    title_tag = soup.find('h2')
    if title_tag:
        raw_title = title_tag.get_text(strip=True)
        car_name = clean_car_name(raw_title)
    else:
        car_name = "Unknown Model"

    # Get price
    price_tag = soup.find('td', class_='ads_price')
    if price_tag:
        price_text = price_tag.get_text(separator=" ", strip=True)
        price_number = price_text.split("€")[0].replace(" ", "").strip()
    else:
        price_number = None

    return car_name, price_number

def is_valid_price(price_text):
    if not price_text:
        return False
    return price_text.isdigit()

def main():
    brand = input("Enter the car brand you want to search for (BMW, Audi, Toyota): ").strip().lower()
    try:
        max_pages = int(input("How many pages would you like to scrape? : ").strip())
    except ValueError:
        print("Invalid input for number of pages. Defaulting to 1.")
        max_pages = 1

    all_links = []
    page = 1
    previous_page_count = 0 

    
    while True:
        try:
            list_url = get_brand_url(brand, page)
            list_html = fetch_html(list_url)
            ad_links = parse_list_page(list_html)

            if not ad_links:
                print(f"No more listings found on page {page}. Stopping.")
                break

            all_links.extend(ad_links)
            print(f"Page {page}: Found {len(ad_links)} listings.")

            # Stop if the current page has fewer listings than the previous page
            if page > 1 and len(ad_links) < previous_page_count:
                print(f"Page {page} has fewer listings ({len(ad_links)}) than the previous page ({previous_page_count}). Stopping.")
                break

            previous_page_count = len(ad_links)
            page += 1

            if page > max_pages:
                print(f"Reached the maximum number of pages ({max_pages}). Stopping.")
                break

        except requests.HTTPError as e:
            print(f"HTTP error on page {page}: {e}")
            break
        except Exception as e:
            print(f"Error on page {page}: {e}")
            break

    print(f"Total listings: {len(all_links)}. Fetching details...")

    results = []

    for link in all_links:
        try:
            ad_html = fetch_html(link)
            car_name, price = parse_ad_page(ad_html)

            if not is_valid_price(price):
                continue  # Skip listings that don't have numeric prices

            print(f"Car: {car_name}")
            print(f"Price: €{price}")
            print(f"Link: {link}")
            print("-" * 40)

            results.append((car_name, f"€{price}", link))

        except Exception as e:
            print(f"Failed to fetch listing {link}: {e}")

    if results:
        # Save scraped data into a CSV file
        os.makedirs("results", exist_ok=True)
        filename = f"results/{brand}_cars.csv"
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Car", "Price", "Link"]) 
            writer.writerows(results)

        print(f"Results saved to {filename}.")
    else:
        print("No valid cars with numeric prices found. No file saved.")

if __name__ == "__main__":
    main()
