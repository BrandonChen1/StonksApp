import requests
from polygon import RESTClient

HEADERS = {
    "User-Agent": "python:subreddit.scraper:v1.0 (by u/anonymous)"
}
client = RESTClient(api_key="lIBofdm9q9wDCLfDg1lsqllOrpeYfC4l")


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
            "id": p["id"],
            "title": p["title"],
            "body": p.get("selftext", ""),
            "comments": p["num_comments"]
        })

    return posts

# Scrape the tickers for a post
def scrapePost(post):
    print(post)
    title = post['title']
    body = post['body']
    comments = scrapeComments(post['id'])


# For a given post, find all the potential ticker symbols for the comments
def scrapeComments(postId):
    url = f"https://www.reddit.com/comments/{postId}.json"
    params = {
        "limit": 10,
        "depth": 10,
        "sort": "top"
    }

    response = requests.get(url, headers=HEADERS, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    comments = []

    def parse_comment_tree(children, depth):
        if depth == 2:
            return
        for child in children:
            kind = child.get("kind")
            data = child.get("data", {})

            # Skip "more" placeholders
            if kind != "t1":
                continue

            comments.append({
                "comment_id": data["id"],
                "body": data.get("body", ""),
                "score": data["score"],
                "created_utc": data["created_utc"],
                "parent_id": data["parent_id"]
            })

            # Recursively parse replies
            replies = data.get("replies")
            if isinstance(replies, dict):
                parse_comment_tree(replies["data"]["children"], depth+1)

    parse_comment_tree(data[1]["data"]["children"], 0)
    return comments

# Find the most frequently mentioned ticker symbols given a list of potential symbols
def countTickers(tickers):
    return tickers

# Validate that these are real tickers by querying https://massive.com/dashboard/keys
# api key lIBofdm9q9wDCLfDg1lsqllOrpeYfC4l
def validateTickers(tickers):
    details = client.get_ticker_details(tickers[0])
    return details


def main():
    subreddits = ["wallstreetbets"]
    posts = scrapeSubreddit(subreddits[0])
    
    scrapePost(posts[0])

    
## EXECUTE
main()
