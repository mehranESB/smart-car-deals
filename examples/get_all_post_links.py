from scraper.utils import open_chrome_and_prepare_search, get_car_article_links

url = "https://divar.ir/s/tehran/car?q=%D8%AA%DB%8C%D8%A8%D8%A7%202"
driver = open_chrome_and_prepare_search()
car_links = get_car_article_links(driver, url)
for link in car_links:
    print(f"- {link}")
print(f"{len(car_links)} links found.")
