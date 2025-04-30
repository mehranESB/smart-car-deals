from .utils import open_chrome_and_prepare_search, get_car_article_links
from .parsers import *
import time
import os
import json


class Scraper:
    def __init__(self, url, name: str, max_num: int = 1000, max_runtime: int = 60):
        self.driver = open_chrome_and_prepare_search()
        self.url = url
        self.name = name
        self.max_num = max_num
        self.max_runtime = max_runtime

        # Create directory for saving scraped data
        self.save_dir = os.path.join("DATA", "scrapeddata", self.name)
        os.makedirs(self.save_dir, exist_ok=True)

    def scrap(self, des=None):
        # get all post links
        post_links = get_car_article_links(
            self.driver, self.url, self.max_num, self.max_runtime
        )

        for i, link in enumerate(post_links):
            try:
                print(f"[{i + 1}/{len(post_links)}] Visiting: {link}")
                self.driver.get(link)
                time.sleep(2)  # small wait for page to load

                # extract data
                title = scrap_title(self.driver)
                imghash = get_post_image_hash(self.driver)
                worked, year, color = scrap_car_details(self.driver)
                price = scrap_base_price(self.driver)

                # prepare final data
                data = {
                    "url": link,
                    "title": title,
                    "imghash": imghash,
                    "worked": worked,
                    "year": year,
                    "color": color,
                    "price": price,
                }

                # define save path
                filename = f"{'post_' + str(i)}.json"
                filepath = os.path.join(self.save_dir, filename)

                # write JSON
                with open(filepath, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)

                print(f"Saved to: {filepath}")

            except Exception as e:
                print(f"❌ Failed to scrape {link}: {e}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Car post scraper")
    parser.add_argument("--url", required=True, help="URL of the listing page")
    parser.add_argument("--name", required=True, help="Project name for saving data")
    parser.add_argument(
        "--max_num", type=int, default=100, help="Maximum number of posts to scrape"
    )
    parser.add_argument(
        "--max_runtime", type=int, default=60, help="Maximum runtime in seconds"
    )

    args = parser.parse_args()

    scraper = Scraper(
        url=args.url, name=args.name, max_num=args.max_num, max_runtime=args.max_runtime
    )
    scraper.scrap()
