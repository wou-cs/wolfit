from app.helpers import pretty_date
from datetime import datetime, timedelta

def test_now():
    assert (pretty_date(datetime.utcnow())) == "just now"


def test_seconds():
    assert (pretty_date(datetime.utcnow() - timedelta(seconds=59))) == " seconds ago"


def test_minute():
    assert (pretty_date(datetime.utcnow() - timedelta(seconds=119))) == "a minute ago"


def test_minutes():
    assert (pretty_date(datetime.utcnow() - timedelta(seconds=3599))) == " minutes ago"


def test_hour():
    assert (pretty_date(datetime.utcnow() - timedelta(seconds=7199))) == "an hour ago"


def test_hours():
    assert (pretty_date(datetime.utcnow() - timedelta(seconds=86399))) == " hours ago"


def test_yesterday():
    assert (pretty_date(datetime.utcnow() - timedelta(days=1))) == "Yesterday"