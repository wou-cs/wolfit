from datetime import datetime
from dateutil import tz
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import markdown
from app import db, login


def pretty_date(time=False):
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    """
    now = datetime.utcnow()
    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time, datetime):
        diff = now - time
    elif not time:
        diff = now - now
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return "just about now"

    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return str(second_diff) + " seconds ago"
        if second_diff < 120:
            return "a minute ago"
        if second_diff < 3600:
            return str(second_diff // 60) + " minutes ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return str(second_diff // 3600) + " hours ago"
    if day_diff == 1:
        return "Yesterday"
    if day_diff < 7:
        return str(day_diff) + " days ago"
    if day_diff < 31:
        return str(day_diff // 7) + " weeks ago"
    if day_diff < 365:
        return str(day_diff // 30) + " months ago"
    return str(day_diff // 365) + " years ago"


user_vote = db.Table(
    "user_vote",
    db.Column("user.id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("post.id", db.Integer, db.ForeignKey("post.id"), primary_key=True),
)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship(
        "Post", order_by="desc(Post.timestamp)", backref="author", lazy="dynamic"
    )
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    post_votes = db.relationship(
        "Post", secondary=user_vote, back_populates="user_votes"
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<User {}>".format(self.username)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))
    vote_count = db.Column(db.Integer, default=0)
    user_votes = db.relationship(
        "User", secondary=user_vote, back_populates="post_votes"
    )

    def __repr__(self):
        return "<Post {}>".format(self.title)

    @classmethod
    def recent_posts(cls):
        return cls.query.order_by(Post.timestamp.desc())

    def body_as_html(self):
        return markdown.markdown(self.body)

    def pretty_timestamp(self):
        return pretty_date(self.timestamp)

    def already_voted(self, user):
        return user in self.user_votes

    def adjust_vote(self, amount):
        if self.vote_count is None:
            self.vote_count = 0
        self.vote_count += amount
        db.session.add(self)

    def up_vote(self, user):
        if self.already_voted(user):
            return
        self.user_votes.append(user)
        self.adjust_vote(1)
        db.session.commit()

    def down_vote(self, user):
        if self.already_voted(user):
            return
        self.user_votes.append(user)
        self.adjust_vote(-1)
        db.session.commit()


class Category(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True, unique=True)
    posts = db.relationship(
        "Post", order_by="desc(Post.timestamp)", backref="category", lazy="dynamic"
    )


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
