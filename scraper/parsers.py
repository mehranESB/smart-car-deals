from .utils import to_persian, to_eng_digits
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import requests
import hashlib


def scrap_title(driver):
    try:
        title_element = driver.find_element(
            By.CSS_SELECTOR,
            "h1.kt-page-title__title.kt-page-title__title--responsive-sized",
        )
        return to_persian(title_element.text.strip())
    except NoSuchElementException:
        return None  # or return "Title not found"


def get_post_image_hash(driver):
    try:
        # Find the image element
        img_element = driver.find_element(
            By.CSS_SELECTOR, "figure.kt-base-carousel__figure img"
        )
        img_url = img_element.get_attribute("src")

        if not img_url:
            print("Image URL not found.")
            return None

        # Download image to memory
        response = requests.get(img_url)
        if response.status_code != 200:
            print(f"Failed to download image: HTTP {response.status_code}")
            return None

        # Compute SHA-256 hash
        image_bytes = response.content
        image_hash = hashlib.sha256(image_bytes).hexdigest()

        return image_hash

    except NoSuchElementException:
        print("Image element not found.")
        return None


def scrap_car_details(driver):
    try:
        # Locate the table row that contains the values
        row = driver.find_element(
            By.CSS_SELECTOR, "table.kt-group-row tbody tr.kt-group-row__data-row"
        )
        cols = row.find_elements(By.CSS_SELECTOR, "td.kt-group-row-item")

        if len(cols) < 3:
            return None  # Incomplete row

        worked, year, color = (
            cols[0].text.strip(),
            cols[1].text.strip(),
            cols[2].text.strip(),
        )

        return to_eng_digits(worked), to_eng_digits(year), to_persian(color)

    except NoSuchElementException:
        print("Details table not found.")
        return None, None, None


def scrap_base_price(driver):
    try:
        # Find all container divs
        rows = driver.find_elements(
            By.CSS_SELECTOR, "div.kt-base-row.kt-base-row--large.kt-unexpandable-row"
        )

        for row in rows:
            title_elem = row.find_element(By.CSS_SELECTOR, ".kt-base-row__title")
            if title_elem.text.strip() == "قیمت پایه":
                value_elem = row.find_element(
                    By.CSS_SELECTOR, ".kt-unexpandable-row__value"
                )
                price_text = value_elem.text.strip()

                if "تومان" in price_text:
                    price_text = price_text.replace("تومان", "").strip()
                    return to_eng_digits(price_text)

        return None  # Not found

    except NoSuchElementException:
        print("Price info not found.")
        return None
