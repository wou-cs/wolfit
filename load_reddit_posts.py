import praw
from datetime import datetime
from app.models import User, Post
from app import app, db, config
from random import randint
import argparse

parser = argparse.ArgumentParser(description='Load posts from a subreddit.')
parser.add_argument('subreddit', metavar='subreddit', nargs='?', default='learnpython',
                    help='the subreddit to load (default is learnpython')
args = parser.parse_args()
subreddit = args.subreddit

app.config.from_object(config.Config)
app.config.from_envvar('WOLFIT_SETTINGS')


def create_user(subreddit):
    username = f"{subreddit}-{randint(0, 999999)}"
    u = User(username=username, email=f"{username}@example.com")
    u.set_password('wolfit')
    db.session.add(u)
    db.session.commit()
    return u


reddit = praw.Reddit()

u = create_user(subreddit)

for submission in reddit.subreddit(subreddit).hot(limit=100):
    # We may have already loaded this post, so check title
    existing = Post.query.filter_by(title=submission.title).first()
    if existing is None:
        p = Post(title=submission.title,
                 body=submission.selftext,
                 timestamp=datetime.utcfromtimestamp(submission.created_utc),
                 user_id=u.id)
        print(f"Creating post: {p}")
        db.session.add(p)
        db.session.commit()
