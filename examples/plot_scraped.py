from scraper.dataset import load_all_posts
from scraper.visual import create_html_plot
import plotly.io as pio

# load all posts
path = "./DATA/scrapeddata/tiba2_1402_02_13"
posts = load_all_posts(path)
posts.sort(key=lambda x: x.get("nameid", 0))

# create html for plot
keyword_groups = [
    ["تیبا"],
    ["۲", "2"],
]
html = create_html_plot(posts, keyword_groups, show=False)
with open(".\DATA\plots\clickable_plot.html", "w") as f:
    f.write(html)
