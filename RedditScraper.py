import requests

HEADERS = {
    "User-Agent": "python:subreddit.scraper:v1.0 (by u/anonymous)"
}

# Scrape the hot posts for a given subreddit
def scrapeSubreddit(subreddit, limit=25):
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


# For a given post, find all the potential ticker symbols for the post
def scrapePost(url):
    tickers = []
    return tickers

# Find the most frequently mentioned ticker symbols given a list of potential symbols
def countTickers(tickers):
    return tickers

# Validate that these are real tickers by querying https://massive.com/dashboard/keys
# api key lIBofdm9q9wDCLfDg1lsqllOrpeYfC4l
def validateTickers(tickers):
    return tickers


def main():
    subreddits = ["wallstreetbets"]
    print(scrapeSubreddit(subreddits[0]))
    
## EXECUTE
main()
