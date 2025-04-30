from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


def scrap_title(driver):
    try:
        title_element = driver.find_element(
            By.CSS_SELECTOR,
            "h1.kt-page-title__title.kt-page-title__title--responsive-sized",
        )
        return title_element.text.strip()
    except NoSuchElementException:
        return None  # or return "Title not found"
