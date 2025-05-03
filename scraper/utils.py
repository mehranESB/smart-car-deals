from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementClickInterceptedException,
)
import time
import arabic_reshaper
from bidi.algorithm import get_display
import os


def open_chrome_and_prepare_search():
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")  # Optional: open in full screen
    chrome_options.add_argument(
        "--disable-blink-features=AutomationControlled"
    )  # Helps bypass bot detection

    # Path to chromedriver
    DRIVER_PATH = "C:\\Users\\Mehran\\Desktop\\github\\cars-divar-scrap\\DATA\\driver\\chromedriver-win64\\chromedriver.exe"
    service = Service(executable_path=DRIVER_PATH)

    # Launch Chrome
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Open the desired search engine
    driver.get("https://www.google.com")

    # Wait a little in case page needs to load
    time.sleep(2)

    return driver  # You can now use `driver.find_element()` to interact with the page


def get_car_article_links(driver, url, max_num=100, max_runtime=60):
    driver.get(url)
    start_time = time.time()
    links = set()

    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        time.sleep(2)

        # 1. Parse articles inside the correct container
        try:
            container = driver.find_element(By.ID, "post-list-container-id")
            articles = container.find_elements(
                By.CSS_SELECTOR, "article.unsafe-kt-post-card"
            )
        except NoSuchElementException:
            break

        for article in articles:
            try:
                anchor = article.find_element(
                    By.CSS_SELECTOR, "a.unsafe-kt-post-card__action"
                )
                href = anchor.get_attribute("href")
                if href and href not in links:
                    links.add(href)
                    if len(links) >= max_num:
                        return list(links)
            except:
                continue  # Skip malformed article

        # 2. Exit if runtime limit is reached
        if (time.time() - start_time) > max_runtime:
            break

        # 3. Try scrolling to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")

        # 4. If no scroll change, try clicking "More Posts" button
        if new_height == last_height:
            try:
                more_btn = driver.find_element(
                    By.CSS_SELECTOR, "button.post-list__load-more-btn-be092"
                )
                if more_btn.is_displayed():
                    try:
                        driver.execute_script(
                            "arguments[0].scrollIntoView(true);", more_btn
                        )
                        more_btn.click()
                        time.sleep(2)  # Let new content load
                        continue  # Try scraping again
                    except ElementClickInterceptedException:
                        pass  # Handle cases where popup/overlay blocks the button
            except NoSuchElementException:
                break  # No button and no scroll = no more content

        last_height = new_height

    return list(links)


def to_persian(exp):
    return get_display(arabic_reshaper.reshape(exp))


def to_eng_digits(text):
    persian_digits = "۰۱۲۳۴۵۶۷۸۹"
    english_digits = "0123456789"

    translation_table = str.maketrans("".join(persian_digits), "".join(english_digits))
    cleaned = (
        text.translate(translation_table).replace("٬", "").replace(",", "").strip()
    )

    try:
        num = int(cleaned)
    except:
        num = None

    return num


def save_html(html, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
