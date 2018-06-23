import praw
from datetime import datetime
from app.models import User, Post
from app import app, db, config
from random import randint


app.config.from_object(config.Config)
app.config.from_envvar('WOLFIT_SETTINGS')


def create_user():
    username = f"python-learner-{randint(0, 999999)}"
    u = User(username=username, email=f"{username}@python.org")
    u.set_password('guido')
    db.session.add(u)
    db.session.commit()
    return u


reddit = praw.Reddit()

u = create_user()

for submission in reddit.subreddit('learnpython').hot(limit=100):
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
