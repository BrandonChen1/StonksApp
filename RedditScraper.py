import requests
from polygon import RESTClient
import time

HEADERS = {
    "User-Agent": "tester 0.1"
}
client = RESTClient(api_key="lIBofdm9q9wDCLfDg1lsqllOrpeYfC4l")


# Scrape the hot posts for a given subreddit
def scrapeSubreddit(subreddit, limit=10):
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
            "num_comments": p["num_comments"]
        })

    return posts

# Scrape the tickers for a post
def scrapePost(post):
    title = post['title']
    body = post['body']
    comments = scrapeComments(post['id'])
    return {
        "title": title,
        "body": body,
        "comments": comments,
    }

# For a given post, find all the potential ticker symbols for the comments
def scrapeComments(postId):
    url = f"https://www.reddit.com/comments/{postId}.json"
    params = {
        "limit": 20,
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
                "body": data.get("body", "")
            })

            # Recursively parse replies
            replies = data.get("replies")
            if isinstance(replies, dict):
                parse_comment_tree(replies["data"]["children"], depth+1)

    parse_comment_tree(data[1]["data"]["children"], 0)
    return comments

# Find all the potential tickers
def findAllTickers(postData):
    allTickers = []

    # Title
    allTickers.extend(findTicker(postData["title"]))

    # Post
    allTickers.extend(findTicker(postData["body"]))

    # Comments
    for comment in postData["comments"]:
        allTickers.extend(findTicker(comment["body"]))
    return allTickers


# Get all potential tickers given a string
def findTicker(string):

    tickers = []
    words = string.split()
    for word in words:
        if not word.isupper() or not word.isalpha():
            continue
        else:
            tickers.append(word)
    return tickers

# Find the most frequently mentioned ticker symbols given a list of potential symbols
def countTickers(tickers):
    return tickers

# Validate that these are real tickers by querying https://massive.com/dashboard/keys
# api key lIBofdm9q9wDCLfDg1lsqllOrpeYfC4l
# 5 requests per minute...
def filterTickers(tickers, seen):
    seen = {} if seen == {} else seen
    filteredTickers = []
    for ticker in tickers:
        if ticker in seen:
            if seen[ticker]:
                filteredTickers.append(ticker)
            continue
        if len(ticker) > 5:
            continue
        try:
            client.get_ticker_details(ticker)
            filteredTickers.append(ticker)
            seen[ticker] = 1
        except Exception as e:
            if "429" in e.args[0]:
                print("hit rate limit, sleeping for 1 minute")
                time.sleep(61)
            seen[ticker] = 0
            print("Could not find ticker symbol: " + ticker)

    return {
        "validTickers": tickers,
        "seen": seen
    }

def main():
    subreddits = ["wallstreetbets"]
    posts = scrapeSubreddit(subreddits[0])
    
    # Loaded the data (title, post, comments) for the posts from a specific subreddit.
    postsData = []
    for post in posts:
        data = scrapePost(post)
        postsData.append(data)
        
    tickers = []

    for postData in postsData:
        tickers.extend(findAllTickers(postData))
    print(tickers)

    
def test():
    tickers = ['WSB', 'WSB', 'OP', 'I', 'JP', 'I', 'JP', 'I', 'LOOK', 'I', 'FINALLY', 'MADE', 'A', 'I', 'I', 'SLV', 'I', 'I', 'SLV', 'I', 'OF', 'YOU', 'WATCHED', 'SLV', 'RIP', 'ARE', 'BEARISH', 'BECAUSE', 'YOU', 'SLV', 'I', 'SLV', 'SLV', 'JP', 'I', 'WSB', 'I', 'XD', 'I', 'I', 'WSB', 'I', 'I', 'I', 'I', 'I', 'DID', 'I', 'I', 'I', 'I', 'I', 'I', 'YOY', 'WSB', 'I', 'I', 'I', 'WSB', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'AI', 'WSB', 'I', 'AI', 'CTO', 'I', 'I', 'I', 'I', 'CTO', 'STEM', 'I', 'LLM', 'AI', 'SDE', 'I', 'A', 'I', 'I', 'I', 'I', 'WSB', 'OP', 'SPY', 'I', 'ROTH', 'WSB', 'I', 'I', 'OP', 'SPY', 'YTD', 'TIL', 'YTD', 'GLD', 'WSB', 'I', 'I', 'I', 'I', 'WSB', 'I', 'SILJ', 'SLV', 'SLV', 'GLD', 'GLD']
    filtered = filterTickers(tickers, {})
    print(filtered)
    
## EXECUTE
# main()
test()
