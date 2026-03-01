import requests
import pandas as pd
import os
import time

OUTPUT_PATH = "../data/shl_catalogue.csv"

API_URL = "https://www.shl.com/api/product-catalog"


def fetch_page(page):

    params = {
        "page": page,
        "pageSize": 12
    }

    response = requests.get(API_URL, params=params)

    if response.status_code != 200:
        return None

    return response.json()


def scrape_all():

    os.makedirs("../data", exist_ok=True)

    all_data = []

    page = 1

    while True:

        print(f"Fetching page {page}")

        data = fetch_page(page)

        if not data or "results" not in data:
            break

        results = data["results"]

        if len(results) == 0:
            break

        for item in results:

            name = item.get("name", "")

            url = "https://www.shl.com" + item.get("url", "")

            description = item.get("shortDescription", "")

            category = item.get("category", "")

            duration = item.get("duration", "")

            test_type = item.get("testType", "")

            all_data.append({
                "assessment_name": name,
                "url": url,
                "description": description,
                "category": category,
                "duration": duration,
                "test_type": test_type
            })

        page += 1

        time.sleep(0.5)

    df = pd.DataFrame(all_data)

    df.to_csv(OUTPUT_PATH, index=False)

    print(f"\n✅ Saved {len(df)} assessments")


if __name__ == "__main__":
    scrape_all()