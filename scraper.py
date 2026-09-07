import os
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://books.toscrape.com/"
OUTPUT_CSV = os.path.join("data", "books.csv")
SUMMARY_FILE = os.path.join("output", "scraping_summary.txt")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; CodeAlpha-Task1-WebScraper/1.0)"
}

def scrape_books():
    records = []
    url = BASE_URL
    page_count = 0

    session = requests.Session()
    session.headers.update(HEADERS)

    while url:
        page_count += 1
        print(f"Scraping page {page_count}: {url}")

        response = session.get(url, timeout=20)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        products = soup.select("article.product_pod")

        for product in products:
            title_tag = product.select_one("h3 a")
            price_tag = product.select_one(".price_color")
            availability_tag = product.select_one(".availability")
            rating_tag = product.select_one("p.star-rating")

            title = title_tag.get("title", "").strip() if title_tag else ""
            price = price_tag.get_text(strip=True) if price_tag else ""
            availability = availability_tag.get_text(" ", strip=True) if availability_tag else ""
            rating = ""
            if rating_tag:
                classes = rating_tag.get("class", [])
                rating = next((c for c in classes if c != "star-rating"), "")

            product_url = urljoin(url, title_tag.get("href", "")) if title_tag else ""

            records.append({
                "title": title,
                "price": price,
                "availability": availability,
                "rating": rating,
                "product_url": product_url
            })

        next_link = soup.select_one("li.next a")
        url = urljoin(url, next_link["href"]) if next_link else None
        time.sleep(0.2)

    return records, page_count

def main():
    os.makedirs("data", exist_ok=True)
    os.makedirs("output", exist_ok=True)

    try:
        records, pages = scrape_books()
    except requests.RequestException as exc:
        print(f"Network error: {exc}")
        print("Check your internet connection and try again.")
        return

    df = pd.DataFrame(records)
    df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")

    with open(SUMMARY_FILE, "w", encoding="utf-8") as f:
        f.write("CodeAlpha Task 1 — Web Scraping Summary\n")
        f.write("=" * 45 + "\n")
        f.write(f"Source: {BASE_URL}\n")
        f.write(f"Pages scraped: {pages}\n")
        f.write(f"Records collected: {len(df)}\n")
        f.write(f"Columns: {', '.join(df.columns)}\n")

    print("\nScraping completed successfully.")
    print(f"Records collected: {len(df)}")
    print(f"CSV saved to: {OUTPUT_CSV}")
    print(f"Summary saved to: {SUMMARY_FILE}")

if __name__ == "__main__":
    main()
