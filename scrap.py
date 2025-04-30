from scraper.scraper import Scraper

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Car post scraper")
    parser.add_argument(
        "--url", type=str, required=True, help="URL of the listing page"
    )
    parser.add_argument(
        "--name", type=str, required=True, help="Project name for saving data"
    )
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


# example :
# python scrap.py --name tiba2 --max_num 10 --max_runtime 60 --url https://divar.ir/s/tehran/car?q=%D8%AA%DB%8C%D8%A8%D8%A7%202
