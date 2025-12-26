import requests

subreddits = ["wallstreetbets"]
HEADERS = {
    "User-Agent": "python:subreddit.scraper:v1.0 (by u/anonymous)"
}


def scrape_subreddit(subreddit, limit=25):
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    params = {"limit": limit}

    response = requests.get(url, headers=HEADERS, params=params, timeout=10)
    response.raise_for_status()

    data = response.json()

    posts = []
    for post in data["data"]["children"]:
        p = post["data"]
        posts.append({
            "title": p["title"],
            "score": p["score"],
            "comments": p["num_comments"],
            "url": "reddit.com" + p["permalink"]
        })

    return posts

print(scrape_subreddit(subreddits[0]))