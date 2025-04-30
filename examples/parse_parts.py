from scraper.utils import open_chrome_and_prepare_search
from scraper.parsers import *
import time

driver = open_chrome_and_prepare_search()

# get the link of post
url = "https://divar.ir/v/%D8%AA%DB%8C%D8%A8%D8%A7-2-%D9%87%D8%A7%DA%86%D8%A8%DA%A9-sx-%D9%85%D8%AF%D9%84-1397/AaQg6GR-"
driver.get(url)
time.sleep(2)

# print title
title = scrap_title(driver)
print(f"title: {title}")

# print sha256 of image
imghash = get_post_image_hash(driver)
print(f"image hash: {imghash}")

# print details
worked, year, color = scrap_car_details(driver)
print(f"worked: {worked}")
print(f"year: {year}")
print(f"color: {color}")

# print price
price = scrap_base_price(driver)
print(f"price: {price}")
