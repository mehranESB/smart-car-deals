from scraper import Scraper

scraper = Scraper(
    url="https://divar.ir/s/tehran/car?q=%D8%AA%D8%A8%D8%A7%202",  # URL containing all car listings
    name="my_project",  # Name of your project (creates ./DATA/scrapdata/my_project directory)
    max_num=1000,  # Maximum number of posts to scrape
    max_runtime=15 * 60,  # Maximum runtime in seconds (15 minutes)
)

scraper.scrap()
