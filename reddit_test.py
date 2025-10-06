import praw
import pandas as pd
from time import sleep
from datetime import datetime

# ✅ Reddit API setup
reddit = praw.Reddit(
    client_id="iJEaWwY_AHHvzzQ9sGXFnQ",
    client_secret="FZNtJVhs04KlWw_tbLsSyiDdM5HvuA",
    user_agent="tuntutan178-sentiment/0.3 by el_manu"
)

# ✅ List of Indonesian-focused subreddits
subreddits = [
    "Indonesia", "indonesia", "Indo", "anakindonesia",
    "IndonesiaPolitics", "IDnews", "indonesia_reddit",
    "Surabaya", "Jakarta", "Bandung", "Yogyakarta", "Bali",
    "kopireddit", "memeIndonesia", "IndoDankMemes"
]

# ✅ List of search queries
queries = [
    "tuntutan 17+8",
    "tuntutan 17 + 8",
    "aksi 17+8",
    "aksi 17 + 8",
    "gerakan 17+8",
    "gerakan 17 + 8",
    "demo 17+8",
    "demo 17 + 8",
    "17+8",
    "17 + 8",
    "tuntutan rakyat 17+8"
]

posts = []
seen_ids = set()  # Avoid duplicates globally

# ✅ Start crawling
for subreddit in subreddits:
    for query in queries:
        print(f"🔍 Searching '{query}' in r/{subreddit}")
        try:
            for submission in reddit.subreddit(subreddit).search(query, sort="new", time_filter="all", limit=150):
                if submission.id not in seen_ids:
                    posts.append({
                        "id": submission.id,
                        "title": submission.title,
                        "text": submission.selftext,
                        "subreddit": subreddit,
                        "score": submission.score,
                        "num_comments": submission.num_comments,
                        "created_utc": datetime.utcfromtimestamp(submission.created_utc),
                        "url": submission.url
                    })
                    seen_ids.add(submission.id)
            sleep(2)  # Respect API rate limits
        except Exception as e:
            print(f"⚠️ Error on r/{subreddit} ({query}): {e}")
            sleep(5)

# ✅ Wrap up
df = pd.DataFrame(posts)
df.drop_duplicates(subset=["id"], inplace=True)
df.to_csv("reddit_tuntutan178_indonesia.csv", index=False, encoding="utf-8-sig")

print(f"\n✅ Total unique posts collected: {len(df)}")
print("📁 Saved to reddit_tuntutan178_indonesia.csv")
