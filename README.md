# 🚗 Smart Car Deal Finder: Scraping & Visualizing Used Car Prices

**Smart Car Deal Finder** is a Python tool that scrapes used car listings from [**Divar.ir**](https://divar.ir/s/tehran), a popular second-hand sales website in Iran. It collects data on car prices, makes, models, and conditions, then visualizes this information for easy comparison. This interactive tool helps users find the best deals and make informed decisions when buying a used car.

<iframe src="./images/clickable_plot.html" width="100%" height="500px" frameborder="0"></iframe>

**Scatter plot visualizing used car prices:** The X-axis represents the car's kilometers driven (KM), while the Y-axis shows the price. The color map indicates the year of manufacture, with different colors corresponding to different years, helping to highlight trends between mileage, price, and age of the car.

## 🧩 Installation

1. Clone the repository:
```bash
git clone https://github.com/mehranESB/smart-car-deals.git
cd smart-car-deals
```

2. Install the project using `setup.py`:
```bash
pip install .
```

## 📚 Usage Guide

** 1️⃣ Scrape All Posts and Save as JSON**

This example demonstrates how to scrape all the car listings from a specific search page on Divar.ir and save them as JSON data.
```python
from scraper import Scraper

scraper = Scraper(
    url="https://divar.ir/s/tehran/car?q=%D8%AA%D8%A8%D8%A7%202", # URL containing all car listings
    name="my_project", # Name of your project (creates ./DATA/scrapdata/my_project directory)
    max_num=1000, # Maximum number of posts to scrape
    max_runtime=15 * 60, # Maximum runtime in seconds (15 minutes)
)

scraper.scrap()
```

** 2️⃣ Visualize and Compare Using Plot**

This example demonstrates how to visualize and compare the scraped data with an interactive plot using `plotly`.
```python
from scraper.dataset import load_all_posts
from scraper.visual import create_html_plot

# Load all scraped posts
path = "./DATA/scrapeddata/tiba2_1402_02_13"
posts = load_all_posts(path)
posts.sort(key=lambda x: x.get("nameid", 0))

# Create HTML for the plot
keyword_groups = [
    ["تیبا"],
    ["۲", "2"],
]
html = create_html_plot(posts, keyword_groups, show=False)

# Save the interactive plot as an HTML file
with open("./DATA/plots/clickable_plot.html", "w") as f:
    f.write(html)
```

> **Note:** For more detailed examples and additional customization options, please refer to the example folder in the repository.


## 🤝 Contributing
Contributions are welcome and appreciated!

Feel free to fork the repository, submit pull requests, or open issues for bugs, feature suggestions, or improvements.

## 📄 License
This project is licensed under the MIT License.
See the `LICENSE.txt` file for details.