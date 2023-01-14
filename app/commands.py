import click
import praw
from datetime import datetime
from random import randint
from flask import Blueprint
from flask.cli import with_appcontext

# from app import app

sample_data = Blueprint("sample_data", __name__)


@sample_data.cli.command("load")
@click.option("-s", "--subreddit", default="learnpython")
def load(subreddit):
    from app import app, db
    from app.models import Post

    """ Loads sample data from the specified subreddit """
    print(f"Loading data from: {subreddit}")
    reddit = praw.Reddit()

    u = create_user(db, subreddit)
    print(f"Created user: {u.username}")
    c = create_category(db, subreddit)

    for submission in reddit.subreddit(subreddit).hot(limit=100):
        # We may have already loaded this post, so check title
        existing = Post.query.filter_by(title=submission.title).first()
        if existing is None:
            link = False
            url = None
            if "reddit.com" not in submission.url:
                link = True
                url = submission.url

            p = Post(
                title=submission.title,
                     body=submission.selftext,
                     timestamp=datetime.utcfromtimestamp(submission.created_utc),
                    vote_count=0,
                    link=link,
                    url=url,
                    user_id=u.id,
                category_id=c.id,
            )
            print(f"Creating post: {p} with url {p.url} in {c.title}")
            db.session.add(p)
            db.session.commit()


def create_user(db, subreddit):
    from app.models import User

    username = f"{subreddit}-{randint(0, 999999)}"
    u = User(username=username, email=f"{username}@example.com")
    u.set_password("wolfit")
    db.session.add(u)
    db.session.commit()
    return u


def create_category(db, subreddit):
    from app.models import Category

    category = None
    category = Category.query.filter_by(title=subreddit).first()
    if category is None:
        category = Category(title=subreddit)
        db.session.add(category)
        db.session.commit()
    return category
