from app.helpers import pretty_date
from datetime import datetime, timedelta

#++ Testing for timestamps in the past day
def test_now():
    assert (pretty_date(datetime.utcnow())) == "just now"


def test_seconds():
    assert (pretty_date(datetime.utcnow() - timedelta(seconds=59))) == "59 seconds ago"


def test_minute():
    assert (pretty_date(datetime.utcnow() - timedelta(seconds=119))) == "a minute ago"


def test_minutes():
    assert (pretty_date(datetime.utcnow() - timedelta(seconds=3599))) == "59 minutes ago"


def test_hour():
    assert (pretty_date(datetime.utcnow() - timedelta(seconds=7199))) == "an hour ago"


def test_hours():
    assert (pretty_date(datetime.utcnow() - timedelta(seconds=86399))) == "23 hours ago"

#--
def test_day_now():
    assert (pretty_date(datetime.utcnow() - timedelta(days=-1))) == "just about now"


def test_day_yesterday():
    assert (pretty_date(datetime.utcnow() - timedelta(days=1))) == "Yesterday"


def test_day_days():
    assert (pretty_date(datetime.utcnow() - timedelta(days=4))) == "4 days ago"


def test_day_weeks():
    assert (pretty_date(datetime.utcnow() - timedelta(days=15))) == "2 weeks ago"


def test_day_months():
    assert (pretty_date(datetime.utcnow() - timedelta(days=95))) == "3 months ago"


def test_day_years():
    assert (pretty_date(datetime.utcnow() - timedelta(days=750))) == "2 years ago"








