import requests
from bs4 import BeautifulSoup
import csv
import sys
import re
import os
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin

BASE_URL = "https://www.advisorkhoj.com"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
}

def extract_emails_from_page(city, page):
    url = f"{BASE_URL}/{city}/Mutual-Fund-Advisor/{page}" if page > 1 else f"{BASE_URL}/{city}/Mutual-Fund-Advisor"
    print(f"🔎 Scanning page {page} → {url}")
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        # Find all <a href="mailto:...">
        anchors = soup.find_all("a", href=re.compile(r"^mailto:"))
        emails = [a["href"].replace("mailto:", "").strip() for a in anchors]
        return emails
    except Exception as e:
        print(f"⚠️ Failed to parse {url}: {e}")
        return []

def get_total_pages(city):
    url = f"{BASE_URL}/{city}/Mutual-Fund-Advisor"
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        pagination = soup.select("ul.pagination li a[href]")
        last_pages = [int(a.text) for a in pagination if a.text.isdigit()]
        return max(last_pages) if last_pages else 1
    except Exception:
        return 1

def main(city):
    city = city.strip().replace(" ", "-")
    total_pages = get_total_pages(city)
    print(f"🌐 Total pages: {total_pages}")
    # csv_filename = f"advisor_emails_{city}.csv"
    # csv_path = os.path.join(app.root_path, "static", csv_filename)

    all_emails = set()
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = executor.map(lambda p: extract_emails_from_page(city, p), range(1, total_pages + 1))
        for email_list in futures:
            all_emails.update(email_list)

    print(f"\n✅ Extracted {len(all_emails)} unique emails.")
    return all_emails
    # with open(csv_path, "w", newline="") as f:
    #     writer = csv.writer(f)
    #     writer.writerow(["Email"])
    #     for email in sorted(all_emails):
    #         writer.writerow([email])

    # print("📁 Saved to advisor_emails.csv")

# if __name__ == "__main__":
#     if len(sys.argv) < 2:
#         print("Invalid command argument")
#     else:
#         main(sys.argv[1])