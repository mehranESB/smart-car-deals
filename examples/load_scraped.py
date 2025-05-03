from scraper.dataset import load_all_posts

# load all posts
path = "./DATA/scrapeddata/tiba2_1402_02_13"
posts = load_all_posts(path)
posts.sort(key=lambda x: x.get("nameid", 0))

# print a post
post = posts[10]
for key, value in post.items():
    print(f"{key}: {value}")
