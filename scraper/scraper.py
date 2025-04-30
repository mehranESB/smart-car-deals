from .utils import open_chrome_and_prepare_search, get_car_article_links
import time


class Scraper:
    def __init__(self, url, max_num: int = 1000, max_runtime: int = 60):
        self.driver = open_chrome_and_prepare_search()
        self.url = url
        self.max_num = max_num
        self.max_runtime = max_runtime

    def scrap(self, des):
        # get all posts
        post_links = get_car_article_links(
            self.driver, self.url, self.max_num, self.max_runtime
        )

        # scrap loop
        for i, link in enumerate(post_links):
            try:
                print(f"[{i}/{len(post_links)}] Visiting: {link}")

                # load post
                self.driver.get(link)
                time.sleep(2)

                # scrap tilte

            except Exception as e:
                print(f"Failed to scrape {link}: {e}")
