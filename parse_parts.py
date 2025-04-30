from scraper.utils import open_chrome_and_prepare_search, to_persian
from scraper.parsers import *
import time

driver = open_chrome_and_prepare_search()

url = "https://divar.ir/v/%D8%AA%DB%8C%D8%A8%D8%A7-2-%D9%87%D8%A7%DA%86%D8%A8%DA%A9-sx-%D9%85%D8%AF%D9%84-1397/AaQg6GR-"
driver.get(url)
time.sleep(2)

title = scrap_title(driver)
print(f"title: {to_persian(title)}")
